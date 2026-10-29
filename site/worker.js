// Test-stage accounts and votes. One shared login (admin / password unless
// ADMIN_USER / ADMIN_PASS are set); every login starts its own session, and
// a session is one voter. Anyone who knows the password can vote, and can
// log in again to vote again, so these numbers are a test.

import REVEAL from "./reveal.generated.js";

const COOKIE = "vellery_session";
const MONTH = 60 * 60 * 24 * 30;
const PER_HOUR = 300;
const TOKEN = /^[a-f0-9]{32}$/;
const PREFIX = /^[a-z0-9-]{3,60}$/;

let ready;
let known;

const json = (body, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store", ...headers },
  });

function setup(env) {
  ready ??= env.DB.batch([
    env.DB.prepare("CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, at TEXT NOT NULL)"),
    env.DB.prepare(
      "CREATE TABLE IF NOT EXISTS votes (item TEXT NOT NULL, voter TEXT NOT NULL, vote INTEGER NOT NULL CHECK (vote IN (1, -1)), basic INTEGER NOT NULL DEFAULT 0, at TEXT NOT NULL, PRIMARY KEY (item, voter))",
    ),
  ]);
  return ready;
}

// Items the site lets people vote on, and whether they can also be marked
// "not meeting basic standard". Built into dist/items.json.
async function votable(env, url) {
  if (!known) {
    const res = await env.ASSETS.fetch(new URL("/items.json", url));
    known = await res.json();
  }
  return known;
}

async function digest(text) {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)));
}

async function same(a, b) {
  const [x, y] = await Promise.all([digest(a), digest(b)]);
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

async function sessionOf(request, env) {
  const m = (request.headers.get("cookie") ?? "").match(new RegExp(`${COOKIE}=([a-f0-9]{32})`));
  if (!m || !TOKEN.test(m[1])) return null;
  const row = await env.DB.prepare("SELECT token FROM sessions WHERE token = ?").bind(m[1]).first();
  return row ? m[1] : null;
}

const cookie = (value, url, maxAge) =>
  `${COOKIE}=${value}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAge}${url.protocol === "https:" ? "; Secure" : ""}`;

async function readJson(request) {
  if (!(request.headers.get("content-type") ?? "").includes("application/json")) return null;
  const raw = await request.text();
  if (raw.length > 500) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function fold(rows, mine) {
  const out = {};
  for (const r of rows) out[r.item] = { up: r.up, down: r.down, basic: r.basic, mine: null };
  for (const r of mine) {
    out[r.item] ??= { up: 0, down: 0, basic: 0, mine: null };
    out[r.item].mine = { vote: r.vote, basic: !!r.basic };
  }
  return out;
}

const TALLY =
  "SELECT item, COALESCE(SUM(vote = 1), 0) AS up, COALESCE(SUM(vote = -1), 0) AS down, COALESCE(SUM(basic), 0) AS basic FROM votes";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    await setup(env);
    const path = url.pathname;

    if (path === "/api/login" && request.method === "POST") {
      const body = await readJson(request);
      const ok =
        body &&
        typeof body.user === "string" &&
        typeof body.password === "string" &&
        (await same(body.user, env.ADMIN_USER ?? "admin")) &&
        (await same(body.password, env.ADMIN_PASS ?? "password"));
      if (!ok) return json({ error: "wrong user or password" }, 401);
      const token = [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, "0")).join("");
      await env.DB.batch([
        env.DB.prepare("DELETE FROM sessions WHERE at < datetime('now', '-30 days')"),
        env.DB.prepare("INSERT INTO sessions (token, at) VALUES (?, datetime('now'))").bind(token),
      ]);
      return json({ user: "admin" }, 200, { "set-cookie": cookie(token, url, MONTH) });
    }

    if (path === "/api/logout" && request.method === "POST") {
      const token = await sessionOf(request, env);
      if (token) await env.DB.prepare("DELETE FROM sessions WHERE token = ?").bind(token).run();
      return json({ ok: true }, 200, { "set-cookie": cookie("", url, 0) });
    }

    if (path === "/api/me" && request.method === "GET") {
      return (await sessionOf(request, env)) ? json({ user: "admin" }) : json({ user: null });
    }

    if (path === "/api/vote" && request.method === "POST") {
      const voter = await sessionOf(request, env);
      if (!voter) return json({ error: "log in to vote" }, 401);
      const body = await readJson(request);
      const { item, vote, basic } = body ?? {};
      if (![1, -1, 0].includes(vote)) return json({ error: "bad input" }, 400);
      const allowed = (await votable(env, url))[item];
      if (!allowed) return json({ error: "this item can't be voted on" }, 404);
      if (basic && (vote !== -1 || !allowed.basic)) return json({ error: "bad input" }, 400);

      const recent = await env.DB.prepare(
        "SELECT COUNT(*) AS n FROM votes WHERE voter = ? AND at > datetime('now', '-1 hour')",
      ).bind(voter).first();
      if (recent.n >= PER_HOUR) return json({ error: "slow down" }, 429);

      if (vote === 0) {
        await env.DB.prepare("DELETE FROM votes WHERE item = ? AND voter = ?").bind(item, voter).run();
      } else {
        await env.DB.prepare(
          "INSERT INTO votes (item, voter, vote, basic, at) VALUES (?, ?, ?, ?, datetime('now')) ON CONFLICT (item, voter) DO UPDATE SET vote = excluded.vote, basic = excluded.basic, at = excluded.at",
        ).bind(item, voter, vote, basic ? 1 : 0).run();
      }
      const { results } = await env.DB.prepare(`${TALLY} WHERE item = ? GROUP BY item`).bind(item).all();
      const { results: mine } = await env.DB.prepare("SELECT item, vote, basic FROM votes WHERE item = ? AND voter = ?")
        .bind(item, voter).all();
      return json(fold(results, mine)[item] ?? { up: 0, down: 0, basic: 0, mine: null });
    }

    // Which model made each blind drawing. Only the Worker holds this; pages never contain it.
    if (path === "/api/reveal" && request.method === "GET") {
      const task = url.searchParams.get("task") ?? "";
      if (!PREFIX.test(task)) return json({ error: "bad task" }, 400);
      const out = {};
      for (const [id, who] of Object.entries(REVEAL)) if (id.startsWith(`${task}.`)) out[id] = who;
      return json(out);
    }

    if (path === "/api/votes" && request.method === "GET") {
      const task = url.searchParams.get("task") ?? "";
      if (!PREFIX.test(task)) return json({ error: "bad task" }, 400);
      const like = `${task}.%`;
      const voter = await sessionOf(request, env);
      const { results } = await env.DB.prepare(`${TALLY} WHERE item LIKE ? GROUP BY item`).bind(like).all();
      const { results: mine } = voter
        ? await env.DB.prepare("SELECT item, vote, basic FROM votes WHERE voter = ? AND item LIKE ?").bind(voter, like).all()
        : { results: [] };
      return json(fold(results, mine));
    }

    return json({ error: "not found" }, 404);
  },
};

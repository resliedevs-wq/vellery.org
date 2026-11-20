// Anonymous ratings. A visitor's first vote or reveal starts a session held in
// an HttpOnly cookie; a session is one voter. New sessions are capped per
// network per hour and votes per session per hour, which keeps casual ballot
// stuffing out without asking anyone to sign up.

import REVEAL from "./reveal.generated.js";

const COOKIE = "vellery_session";
const YEAR = 60 * 60 * 24 * 365;
const SESSIONS_PER_HOUR = 20;
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
    env.DB.prepare("CREATE TABLE IF NOT EXISTS drawing_reveals (voter TEXT NOT NULL, item TEXT NOT NULL, PRIMARY KEY(voter,item))"),
    env.DB.prepare("CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, at TEXT NOT NULL)"),
    env.DB.prepare("CREATE TABLE IF NOT EXISTS session_starts (origin TEXT NOT NULL, at TEXT NOT NULL)"),
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

async function sessionOf(request, env) {
  const m = (request.headers.get("cookie") ?? "").match(new RegExp(`${COOKIE}=([a-f0-9]{32})`));
  if (!m || !TOKEN.test(m[1])) return null;
  const row = await env.DB.prepare("SELECT token FROM sessions WHERE token = ?").bind(m[1]).first();
  return row ? m[1] : null;
}

const hex = (bytes) => [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");

// The visitor's session, starting one if they have none yet. Returns the
// Set-Cookie header to send back when a session was just created.
async function ensureSession(request, env, url) {
  const existing = await sessionOf(request, env);
  if (existing) return { voter: existing, headers: {} };
  const ip = request.headers.get("cf-connecting-ip") ?? "local";
  const origin = hex(new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(`vellery:${ip}`)))).slice(0, 32);
  const recent = await env.DB.prepare(
    "SELECT COUNT(*) AS n FROM session_starts WHERE origin = ? AND at > datetime('now', '-1 hour')",
  ).bind(origin).first();
  if (recent.n >= SESSIONS_PER_HOUR) return { voter: null, headers: {} };
  const token = hex(crypto.getRandomValues(new Uint8Array(16)));
  await env.DB.batch([
    env.DB.prepare("DELETE FROM session_starts WHERE at < datetime('now', '-1 day')"),
    env.DB.prepare("INSERT INTO session_starts (origin, at) VALUES (?, datetime('now'))").bind(origin),
    env.DB.prepare("INSERT INTO sessions (token, at) VALUES (?, datetime('now'))").bind(token),
  ]);
  return { voter: token, headers: { "set-cookie": cookie(token, url, YEAR) } };
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

    if (path === "/api/vote" && request.method === "POST") {
      const body = await readJson(request);
      const { item, vote, basic } = body ?? {};
      if (![1, -1, 0].includes(vote)) return json({ error: "bad input" }, 400);
      const allowed = (await votable(env, url))[item];
      if (!allowed) return json({ error: "this item can't be voted on" }, 404);
      if (basic && (vote !== -1 || !allowed.basic)) return json({ error: "bad input" }, 400);
      const { voter, headers } = await ensureSession(request, env, url);
      if (!voter) return json({ error: "too many new visitors from this network, try again later" }, 429);

      const recent = await env.DB.prepare(
        "SELECT COUNT(*) AS n FROM votes WHERE voter = ? AND at > datetime('now', '-1 hour')",
      ).bind(voter).first();
      if (recent.n >= PER_HOUR) return json({ error: "slow down" }, 429);

      // Check exposure in the mutation so an overlapping reveal cannot let a
      // late vote through. Revealing a drawing preserves any earlier vote.
      const blind = "NOT EXISTS (SELECT 1 FROM drawing_reveals WHERE voter = ? AND item = ?)";
      const changed = vote === 0
        ? await env.DB.prepare(`DELETE FROM votes WHERE item = ? AND voter = ? AND ${blind}`)
            .bind(item, voter, voter, item).run()
        : await env.DB.prepare(
            `INSERT INTO votes (item, voter, vote, basic, at) SELECT ?, ?, ?, ?, datetime('now') WHERE ${blind}
             ON CONFLICT (item, voter) DO UPDATE SET vote = excluded.vote, basic = excluded.basic, at = excluded.at`,
          ).bind(item, voter, vote, basic ? 1 : 0, voter, item).run();
      if (!changed.meta.changes && REVEAL[item] && await env.DB.prepare(
        "SELECT 1 FROM drawing_reveals WHERE voter = ? AND item = ?",
      ).bind(voter, item).first()) return json({error: "model already revealed"}, 409, headers);

      const { results } = await env.DB.prepare(`${TALLY} WHERE item = ? GROUP BY item`).bind(item).all();
      const { results: mine } = await env.DB.prepare("SELECT item, vote, basic FROM votes WHERE item = ? AND voter = ?")
        .bind(item, voter).all();
      return json(fold(results, mine)[item] ?? { up: 0, down: 0, basic: 0, mine: null }, 200, headers);
    }

    // Which model made each blind drawing. Only the Worker holds this; pages never contain it.
    if (path === "/api/reveal" && request.method === "POST") {
      const {task, ids} = await request.json().catch(() => null) ?? {};
      if (typeof task !== "string" || !PREFIX.test(task) || !Array.isArray(ids) || !ids.length ||
          ids.some(id => typeof id !== "string" || !id.startsWith(task + ".") || !REVEAL[id])) {
        return json({error: "unknown drawings"}, 400);
      }
      const { voter, headers } = await ensureSession(request, env, url);
      if (voter) await env.DB.prepare(
        "INSERT OR IGNORE INTO drawing_reveals(voter,item) SELECT ?, value FROM json_each(?)",
      ).bind(voter, JSON.stringify(ids)).run();
      return json(Object.fromEntries(ids.map(id => [id, REVEAL[id]])), 200, headers);
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
      const tallies = fold(results, mine);
      if (voter) {
        const {results: seen} = await env.DB.prepare(
          "SELECT item FROM drawing_reveals WHERE voter = ? AND item LIKE ?",
        ).bind(voter, like).all();
        for (const {item} of seen) {
          tallies[item] ??= {up: 0, down: 0, basic: 0, mine: null};
          tallies[item].revealed = REVEAL[item];
        }
      }
      return json(tallies);
    }

    return json({ error: "not found" }, 404);
  },
};

// Visitor ratings for the test stage. No sign-in: a voter is a random token
// the browser makes up, so anyone can vote, and anyone can mint more voters.
// These numbers are shown next to the graded results, never mixed into them.

const RATINGS = new Set(["good", "fix", "slop"]);
const VOTER = /^[a-f0-9]{32}$/;
const PREFIX = /^[a-z0-9-]{3,60}$/;
const PER_HOUR = 300;

let ready;
let known;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

function setup(env) {
  ready ??= env.DB.prepare(
    "CREATE TABLE IF NOT EXISTS ratings (item TEXT NOT NULL, voter TEXT NOT NULL, rating TEXT NOT NULL CHECK (rating IN ('good', 'fix', 'slop')), at TEXT NOT NULL, PRIMARY KEY (item, voter))",
  ).run();
  return ready;
}

async function knownItems(env, url) {
  if (!known) {
    const res = await env.ASSETS.fetch(new URL("/items.json", url));
    known = new Set(await res.json());
  }
  return known;
}

function fold(rows) {
  const out = {};
  for (const { item, rating, n } of rows) {
    out[item] ??= { good: 0, fix: 0, slop: 0 };
    out[item][rating] = n;
  }
  return out;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    await setup(env);

    if (url.pathname === "/api/rate" && request.method === "POST") {
      const raw = await request.text();
      if (raw.length > 500) return json({ error: "too large" }, 413);
      let body;
      try {
        body = JSON.parse(raw);
      } catch {
        return json({ error: "bad json" }, 400);
      }
      const { item, rating, voter } = body ?? {};
      if (!RATINGS.has(rating) || !VOTER.test(voter ?? "")) return json({ error: "bad input" }, 400);
      if (!(await knownItems(env, url)).has(item)) return json({ error: "unknown item" }, 404);

      const recent = await env.DB.prepare(
        "SELECT COUNT(*) AS n FROM ratings WHERE voter = ? AND at > datetime('now', '-1 hour')",
      ).bind(voter).first();
      if (recent.n >= PER_HOUR) return json({ error: "slow down" }, 429);

      await env.DB.prepare(
        "INSERT INTO ratings (item, voter, rating, at) VALUES (?, ?, ?, datetime('now')) ON CONFLICT (item, voter) DO UPDATE SET rating = excluded.rating, at = excluded.at",
      ).bind(item, voter, rating).run();

      const { results } = await env.DB.prepare(
        "SELECT item, rating, COUNT(*) AS n FROM ratings WHERE item = ? GROUP BY item, rating",
      ).bind(item).all();
      return json(fold(results)[item] ?? { good: 0, fix: 0, slop: 0 });
    }

    if (url.pathname === "/api/ratings" && request.method === "GET") {
      const task = url.searchParams.get("task") ?? "";
      if (!PREFIX.test(task)) return json({ error: "bad task" }, 400);
      const { results } = await env.DB.prepare(
        "SELECT item, rating, COUNT(*) AS n FROM ratings WHERE item LIKE ? GROUP BY item, rating",
      ).bind(`${task}.%`).all();
      return json(fold(results));
    }

    return json({ error: "not found" }, 404);
  },
};

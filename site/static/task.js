(() => {
  const data = JSON.parse(document.getElementById("data").textContent);
  const prompts = [...document.querySelectorAll(".prompt")];
  const tiles = [...document.querySelectorAll(".tile")];
  const groups = Object.fromEntries([...document.querySelectorAll(".group")].map((g) => [g.dataset.g, g]));
  const detail = document.getElementById("detail");
  const rules = data.rules;
  const byId = Object.fromEntries(tiles.map((t) => [t.dataset.id, t]));
  const cacheKey = `vellery.votes.${data.slug}`;
  const pending = {};
  let votes = {};
  let variant = "strong";
  let selected = null;
  let placed = false;

  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };
  const tally = (id) => votes[id] || { up: 0, down: 0, basic: 0, mine: null };

  // Last tallies this browser saw, so the page can order itself before the server answers.
  try {
    const saved = JSON.parse(localStorage.getItem(cacheKey) || "{}");
    for (const [id, v] of Object.entries(saved)) votes[id] = { ...v, mine: null };
  } catch {}
  const remember = () => {
    try {
      localStorage.setItem(cacheKey, JSON.stringify(Object.fromEntries(Object.entries(votes).map(([id, v]) => [id, { up: v.up, down: v.down, basic: v.basic }]))));
    } catch {}
  };

  // Scripted tasks keep their grade. Drawings take theirs from votes.
  function bucketOf(tile) {
    if (data.mode !== "gallery") return tile.dataset.g || tile.closest(".group").dataset.g;
    const v = tally(tile.dataset.id);
    const total = v.up + v.down;
    if (total < rules.min) return "none";
    if (v.up / total >= rules.green) return "good";
    if (v.up / total < rules.red && v.basic > v.down - v.basic) return "slop";
    return "fix";
  }

  function shuffle(list) {
    for (let i = list.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [list[i], list[j]] = [list[j], list[i]];
    }
    return list;
  }

  // Green runs get a new random order on every visit; the others keep theirs.
  function place() {
    const wanted = {};
    tiles.forEach((t) => (wanted[t.dataset.id] = bucketOf(t)));
    for (const [g, box] of Object.entries(groups)) {
      const holder = box.querySelector(".tiles");
      let mine = tiles.filter((t) => wanted[t.dataset.id] === g);
      if (g === "good" && !placed) mine = shuffle(mine);
      for (const t of mine) if (!placed || t.parentNode !== holder) holder.append(t);
    }
    placed = true;
    tiles.forEach((t) => (t.dataset.g = wanted[t.dataset.id]));
  }

  const plain = (v) => v.down - v.basic;

  function refresh() {
    tiles.forEach((t) => {
      t.hidden = t.dataset.variant !== variant;
      t.classList.toggle("on", t.dataset.id === selected);
      const v = tally(t.dataset.id);
      t.querySelector(".score").textContent = [v.up && `▲ ${v.up}`, plain(v) && `▼ ${plain(v)}`, v.basic && `▼▼ ${v.basic}`]
        .filter(Boolean).join("  ");
    });
    Object.values(groups).forEach((box) => {
      const n = [...box.querySelectorAll(".tile")].filter((t) => !t.hidden).length;
      box.hidden = n === 0;
      box.querySelector(".count").textContent = n;
    });
  }

  // The open item sits right under the row of its tile, like a line break in the grid.
  function dock() {
    const tile = selected && byId[selected];
    if (!tile || tile.hidden) {
      detail.hidden = true;
      return;
    }
    const row = [...tile.parentNode.children].filter(
      (c) => c.classList.contains("tile") && !c.hidden && Math.abs(c.offsetTop - tile.offsetTop) < 4,
    );
    row[row.length - 1].after(detail);
    detail.hidden = false;
  }

  function paintVotes() {
    const slot = detail.querySelector(".votes");
    if (!slot || !selected || !data.votable[selected]) return;
    const v = tally(selected);
    const mine = v.mine;
    const button = (cls, label, title, on, next) => {
      const b = el("button", `vote ${cls}${on ? " on" : ""}`, label);
      b.title = title;
      b.setAttribute("aria-label", title);
      b.addEventListener("click", () => vote(selected, on ? null : next));
      return b;
    };
    const bar = el("div", "votebar");
    bar.append(
      button("up", `▲ ${v.up}`, "Upvote", mine && mine.vote === 1, { vote: 1, basic: false }),
      button("down", `▼ ${plain(v)}`, "Downvote", mine && mine.vote === -1 && !mine.basic, { vote: -1, basic: false }),
    );
    if (data.votable[selected].basic)
      bar.append(button("basic", `▼▼ ${v.basic}`, "Not meeting basic standard", mine && mine.basic, { vote: -1, basic: true }));
    slot.replaceChildren(bar);
    if (!window.vellery.me) slot.append(el("span", "note", "Log in to vote"));
  }

  // Redraw everything from `votes`, keeping the open item where it is on screen.
  function render() {
    const before = !detail.hidden ? detail.getBoundingClientRect().top : null;
    place();
    refresh();
    dock();
    paintVotes();
    if (before !== null && !detail.hidden) scrollBy(0, detail.getBoundingClientRect().top - before);
  }

  function applyLocal(v, next) {
    const out = { up: v.up, down: v.down, basic: v.basic, mine: next };
    if (v.mine) {
      if (v.mine.vote === 1) out.up--;
      else {
        out.down--;
        if (v.mine.basic) out.basic--;
      }
    }
    if (next) {
      if (next.vote === 1) out.up++;
      else {
        out.down++;
        if (next.basic) out.basic++;
      }
    }
    return out;
  }

  // The page updates first; the server catches up. A failed save quietly puts things back.
  async function vote(id, next) {
    if (!window.vellery.me) return window.vellery.openLogin();
    const before = tally(id);
    votes[id] = applyLocal(before, next);
    const seq = (pending[id] = (pending[id] || 0) + 1);
    render();
    try {
      const res = await fetch("/api/vote", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ item: id, vote: next ? next.vote : 0, basic: !!(next && next.basic) }),
      });
      if (seq !== pending[id]) return;
      if (!res.ok) throw new Error(res.status);
      votes[id] = await res.json();
      remember();
    } catch (e) {
      if (seq !== pending[id]) return;
      votes[id] = before;
      if (String(e.message) === "401") window.vellery.openLogin();
    }
    render();
  }

  function show(id) {
    selected = id;
    detail.innerHTML = data.detail[id];
    if (data.votable[id]) detail.querySelector(".dhead").after(el("div", "votes"));
    dock();
    refresh();
    paintVotes();
  }

  function pick(next) {
    variant = next;
    prompts.forEach((p) => p.classList.toggle("on", p.dataset.variant === variant));
    selected = null;
    detail.hidden = true;
    refresh();
    if (data.mode !== "gallery") {
      const first = ["fix", "slop"].map((g) => tiles.find((t) => !t.hidden && t.dataset.g === g)).find(Boolean);
      if (first) show(first.dataset.id);
    }
  }

  async function load() {
    try {
      const res = await fetch(`/api/votes?task=${data.slug}`);
      if (res.ok) votes = await res.json();
    } catch {}
    remember();
    render();
  }

  prompts.forEach((p) => p.addEventListener("click", () => pick(p.dataset.variant)));
  tiles.forEach((t) =>
    t.addEventListener("click", () => {
      if (selected === t.dataset.id) {
        selected = null;
        detail.hidden = true;
        refresh();
      } else show(t.dataset.id);
    }),
  );
  let resizing;
  addEventListener("resize", () => {
    clearTimeout(resizing);
    resizing = setTimeout(dock, 100);
  });
  document.addEventListener("vellery:auth", load);

  place();
  pick("strong");
  load();
  window.vellery.ready.then(paintVotes);
})();

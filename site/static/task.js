(() => {
  const data = JSON.parse(document.getElementById("data").textContent);
  const prompts = [...document.querySelectorAll(".prompt")];
  const tiles = [...document.querySelectorAll(".tile")];
  const groups = Object.fromEntries([...document.querySelectorAll(".group")].map((g) => [g.dataset.g, g]));
  const detail = document.getElementById("detail");
  const rules = data.rules;
  const byId = Object.fromEntries(tiles.map((t) => [t.dataset.id, t]));
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

  // Scripted tasks keep their grade. Drawings take theirs from votes.
  function bucketOf(tile) {
    if (data.mode !== "gallery") return tile.dataset.g || tile.closest(".group").dataset.g;
    const v = tally(tile.dataset.id);
    const total = v.up + v.down;
    if (total < rules.min) return "none";
    const share = v.up / total;
    if (share >= rules.green) return "good";
    if (share < rules.red && v.basic > v.down - v.basic) return "slop";
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
    const home = {};
    tiles.forEach((t) => (home[t.dataset.id] = bucketOf(t)));
    Object.entries(groups).forEach(([g, box]) => {
      let mine = tiles.filter((t) => home[t.dataset.id] === g);
      if (g === "good" && !placed) mine = shuffle(mine);
      mine.forEach((t) => {
        if (!placed || t.parentNode !== box.querySelector(".tiles")) box.querySelector(".tiles").append(t);
      });
    });
    placed = true;
    tiles.forEach((t) => {
      t.dataset.g = home[t.dataset.id];
      t.classList.toggle("on", t.dataset.id === selected);
    });
  }

  function refresh() {
    tiles.forEach((t) => {
      t.hidden = t.dataset.variant !== variant;
      const v = tally(t.dataset.id);
      const score = t.querySelector(".score");
      score.textContent = v.up || v.down ? `▲ ${v.up}  ▼ ${v.down}` : "";
    });
    Object.values(groups).forEach((box) => {
      const n = [...box.querySelectorAll(".tile")].filter((t) => !t.hidden).length;
      box.hidden = n === 0;
      box.querySelector(".count").textContent = n;
    });
  }

  async function vote(id, body) {
    if (!window.vellery.me) return window.vellery.openLogin();
    const res = await fetch("/api/vote", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ item: id, ...body }),
    });
    if (res.status === 401) return window.vellery.openLogin();
    if (!res.ok) return;
    votes[id] = await res.json();
    refresh();
    paintVotes();
    // Drawings can change color; move them only when the bucket changes.
    if (data.mode === "gallery") place();
    refresh();
  }

  function paintVotes() {
    const slot = detail.querySelector(".votes");
    if (!slot || !selected || !data.votable[selected]) return;
    const v = tally(selected);
    const mine = v.mine ? v.mine.vote : 0;
    const bar = el("div", "votebar");
    const up = el("button", "vote up" + (mine === 1 ? " on" : ""), `▲ ${v.up}`);
    const down = el("button", "vote down" + (mine === -1 ? " on" : ""), `▼ ${v.down}`);
    up.setAttribute("aria-label", "Upvote");
    down.setAttribute("aria-label", "Downvote");
    up.addEventListener("click", () => vote(selected, { vote: mine === 1 ? 0 : 1 }));
    down.addEventListener("click", () => vote(selected, { vote: mine === -1 ? 0 : -1 }));
    bar.append(up, down);
    if (mine === -1 && data.votable[selected].basic) {
      const basic = el("button", "vote basic" + (v.mine.basic ? " on" : ""), "Not meeting basic standard");
      basic.addEventListener("click", () => vote(selected, { vote: -1, basic: !v.mine.basic }));
      bar.append(basic);
    }
    if (!window.vellery.me) bar.append(el("span", "note", "Log in to vote"));
    slot.replaceChildren(bar);
  }

  function show(id) {
    selected = id;
    tiles.forEach((t) => t.classList.toggle("on", t.dataset.id === id));
    detail.innerHTML = data.detail[id];
    if (data.votable[id]) {
      const slot = el("div", "votes");
      detail.querySelector(".dhead").after(slot);
      paintVotes();
    }
    detail.hidden = false;
  }

  function pick(next) {
    variant = next;
    prompts.forEach((p) => p.classList.toggle("on", p.dataset.variant === variant));
    refresh();
    detail.hidden = true;
    selected = null;
    tiles.forEach((t) => t.classList.remove("on"));
    if (data.mode !== "gallery") {
      const first = ["fix", "slop"].map((g) => tiles.find((t) => !t.hidden && t.dataset.g === g)).find(Boolean);
      if (first) show(first.dataset.id);
    }
  }

  async function load() {
    try {
      const res = await fetch(`/api/votes?task=${data.slug}`);
      votes = res.ok ? await res.json() : {};
    } catch {
      votes = {};
    }
    place();
    refresh();
    if (selected) show(selected);
  }

  prompts.forEach((p) => p.addEventListener("click", () => pick(p.dataset.variant)));
  tiles.forEach((t) =>
    t.addEventListener("click", () => {
      show(t.dataset.id);
      if (detail.getBoundingClientRect().top > innerHeight * 0.75) detail.scrollIntoView({ behavior: "smooth", block: "start" });
    }),
  );
  document.addEventListener("vellery:auth", load);
  window.vellery.ready.then(async () => {
    await load();
    pick("strong");
  });
})();

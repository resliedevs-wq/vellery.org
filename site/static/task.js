(() => {
  const data = JSON.parse(document.getElementById("data").textContent);
  const prompts = [...document.querySelectorAll(".prompt")];
  const tiles = [...document.querySelectorAll(".tile")];
  const groups = Object.fromEntries([...document.querySelectorAll(".group")].map((g) => [g.dataset.g, g]));
  const board = document.getElementById("board");
  const matrixBox = document.getElementById("matrix");
  const legend = document.getElementById("legend");
  const revealBar = document.getElementById("revealbar");
  const rules = data.rules;
  const byId = Object.fromEntries(tiles.map((t) => [t.dataset.id, t]));
  const cacheKey = `vellery.votes.${data.slug}`;
  const metaKey = `vellery.reveal.${data.slug}`;
  const flagKey = `vellery_revealed_${data.slug}`;
  const rank = { good: 0, fix: 1, slop: 2, none: 3 };
  const rowsPlaced = new Set();
  const exposureKey = `vellery.disclosed.v2.${data.slug}`;
  let meta = {};
  let revealing = false;
  const pending = {};
  let votes = {};
  let variant = "strong";
  let selected = null;
  let placed = false;
  let order = [];

  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };
  const tally = (id) => votes[id] || { up: 0, down: 0, basic: 0, mine: null };

  // The viewer: one open item over the page, with arrows to step through the grid.
  const viewer = el("dialog", "viewer");
  viewer.innerHTML =
    '<div class="vwrap"><button class="vnav prev" aria-label="Previous">‹</button>' +
    '<div class="vpanel"><div class="vtop"><span class="num vpos"></span><button class="vclose" aria-label="Close">✕</button></div>' +
    '<div class="vbody"></div></div><button class="vnav next" aria-label="Next">›</button></div>';
  document.body.append(viewer);
  const body = viewer.querySelector(".vbody");

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
    if (data.mode !== "gallery") return tile.dataset.g;
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

  const blind = (t) => data.mode === "gallery" && !meta[t.dataset.id];
  const rowOf = (model) => matrixBox.querySelector(`.mrow[data-model="${model}"]`);

  // Drawings get model rows once the models are revealed.
  function buildRows() {
    for (const m of data.models) {
      if (rowOf(m.id)) continue;
      const row = el("div", "mrow");
      row.dataset.model = m.id;
      row.append(el("div", "mlabel", m.label));
      matrixBox.append(row);
    }
    tiles.forEach((t) => {
      const who = meta[t.dataset.id];
      if (who) {
        t.dataset.model = who.id;
        t.dataset.run = who.run;
        t.setAttribute("aria-label", `${who.label}, run ${who.run}`);
        rowOf(who.id).append(t);
      }
    });
  }

  // In each model's row: usable runs first, in a new random order on every visit,
  // then needs-a-fix, then slop, each in run order.
  function placeRows() {
    matrixBox.querySelectorAll(".mrow").forEach((row) => {
      const model = row.dataset.model;
      const mine = [...row.querySelectorAll(".tile")];
      const good = mine.filter((t) => t.dataset.g === "good");
      if (!rowsPlaced.has(model)) shuffle(good);
      const rest = mine
        .filter((t) => t.dataset.g !== "good")
        .sort((a, b) => rank[a.dataset.g] - rank[b.dataset.g] || a.dataset.run - b.dataset.run);
      [...good, ...rest].forEach((t) => row.append(t));
      rowsPlaced.add(model);
    });
  }

  function placeFlat(wanted) {
    for (const [g, box] of Object.entries(groups)) {
      const holder = box.querySelector(".tiles");
      let mine = tiles.filter((t) => wanted[t.dataset.id] === g && blind(t));
      if (!placed) mine = shuffle(mine);
      for (const t of mine) if (!placed || t.parentNode !== holder) holder.append(t);
    }
  }

  function place() {
    const wanted = {};
    tiles.forEach((t) => (wanted[t.dataset.id] = blind(t) ? "none" : bucketOf(t)));
    tiles.forEach((t) => (t.dataset.g = wanted[t.dataset.id]));
    if (board) {
      board.hidden = !tiles.some((t) => t.dataset.variant === variant && blind(t));
      placeFlat(wanted);
    }
    const hasRows = tiles.some((t) => t.dataset.variant === variant && !blind(t));
    matrixBox.hidden = !hasRows;
    if (legend) legend.hidden = !hasRows;
    if (hasRows) placeRows();
    placed = true;
  }

  function refresh() {
    tiles.forEach((t) => {
      t.hidden = t.dataset.variant !== variant;
      t.classList.toggle("on", t.dataset.id === selected);
      const v = tally(t.dataset.id);
      const indicators = [
        ["good", v.up, "Upvotes"],
        ["fix", v.down - v.basic, "Downvotes"],
        ["slop", v.basic, "Not meeting basic standard"],
      ].filter(([, count]) => count && !blind(t)).map(([grade, count, label]) => {
        const indicator = el("span", `rating ${grade}`, count);
        indicator.title = `${label}: ${count}`;
        indicator.setAttribute("aria-label", indicator.title);
        return indicator;
      });
      t.querySelector(".score").replaceChildren(...indicators);
    });
    Object.values(groups).forEach((box) => {
      const n = [...box.querySelectorAll(".tile")].filter((t) => !t.hidden).length;
      box.hidden = n === 0;
      box.querySelector(".count").textContent = n;
    });
    matrixBox.querySelectorAll(".mrow").forEach((row) => {
      const stats = data.models.find((m) => m.id === row.dataset.model)?.stats?.[variant];
      if (stats) {
        const label = row.querySelector(".mlabel");
        let info = label.querySelector(".mmeta");
        if (!info) {
          info = el("span", "mmeta");
          label.append(info);
        }
        info.textContent = [stats.date, stats.cost].filter(Boolean).join(" · ");
        info.title = "Test date (UTC) · Average estimated API cost per run, including retries";
      }
      row.hidden = ![...row.querySelectorAll(".tile")].some((t) => !t.hidden);
    });
  }

  function blindTiles(which) {
    return tiles.filter((t) => t.dataset.variant === which && blind(t));
  }

  async function reveal(ids) {
    if (revealing || !ids.length) return;
    const subject = ids.length === 1 ? "this drawing" : `these ${ids.length} drawings`;
    if (!window.confirm(`Reveal the model for ${subject}? Your ratings stay saved. Scoring closes for ${subject}.`)) return;
    revealing = true;
    paintReveal();
    try {
      const res = await fetch("/api/reveal", {
        method: "POST", headers: {"content-type": "application/json"},
        body: JSON.stringify({task: data.slug, ids}),
      });
      if (!res.ok) throw new Error();
      const disclosed = await res.json();
      if (!ids.every((id) => disclosed[id])) throw new Error();
      Object.assign(meta, disclosed);
      try {
        Object.assign(meta, JSON.parse(localStorage.getItem(exposureKey) || "{}"));
        localStorage.setItem(exposureKey, JSON.stringify(meta));
      } catch {}
      buildRows();
    } catch {
      window.alert("Could not reveal the models. Please try again.");
    } finally {
      revealing = false;
      render();
    }
  }

  function paintReveal() {
    if (!revealBar) return;
    const here = blindTiles(variant);
    const unrated = here.filter((t) => !tally(t.dataset.id).mine);
    const rate = revealBar.querySelector("#rate");
    rate.disabled = !here.length;
    rate.textContent = here.length && !unrated.length ? "Review your ratings" : "Rate a drawing";
    const revealButton = revealBar.querySelector("#reveal");
    revealButton.hidden = !here.length;
    revealButton.disabled = revealing;
    const status = revealBar.querySelector(".num");
    if (!here.length) {
      status.textContent = "All models have been revealed for this prompt. Blind scoring is closed.";
      return;
    }
    status.textContent = window.vellery.me
      ? `${here.length - unrated.length} of ${here.length} rated blind`
      : `${here.length} anonymous drawings`;
  }

  function paintHeader() {
    const who = selected && meta[selected];
    if (!who) return;
    const head = body.querySelector(".dhead");
    if (!head || head.dataset.revealed) return;
    head.dataset.revealed = "1";
    const title = head.querySelector("h2");
    const kid = title.textContent;
    title.replaceChildren(document.createTextNode(`${who.label} `), el("span", "", `run ${who.run}`));
    head.querySelector(".note").textContent = `Drawing ${kid}`;
  }

  function paintStatus() {
    const chip = body.querySelector(".verdict.status");
    if (!chip || !selected) return;
    chip.hidden = blind(byId[selected]);
    if (chip.hidden) return;
    const v = tally(selected);
    const b = bucketOf(byId[selected]);
    chip.className = `verdict status ${b}`;
    chip.replaceChildren(document.createTextNode(data.buckets[b]));
    if (v.up + v.down) chip.append(el("small", "", `${v.up} of ${v.up + v.down} up`));
  }

  function paintVotes() {
    const slot = body.querySelector(".votes");
    if (!slot || !selected || !data.votable[selected]) return;
    if (meta[selected]) {
      slot.replaceChildren(el("span", "note", "Model revealed · scoring closed"));
      return;
    }
    const v = tally(selected);
    const mine = v.mine;
    const downed = !!mine && mine.vote === -1;
    const button = (cls, label, title, on, next) => {
      const b = el("button", `vote ${cls}${on ? " on" : ""}`, label);
      b.title = title;
      b.setAttribute("aria-label", title);
      b.addEventListener("click", () => vote(selected, next));
      return b;
    };
    const bar = el("div", "votebar");
    const label = (symbol, count) => blind(byId[selected]) ? symbol : `${symbol} ${count}`;
    // ▼▼ replaces ▼: one voter is one vote, counted at whichever level they chose.
    bar.append(
      button("up", label("▲", v.up), "Upvote", mine && mine.vote === 1, mine && mine.vote === 1 ? null : { vote: 1, basic: false }),
      button("down", label("▼", v.down - v.basic), "Downvote", downed && !mine.basic, downed && !mine.basic ? null : { vote: -1, basic: false }),
    );
    if (downed && data.votable[selected].basic)
      bar.append(button("basic", label("▼▼", v.basic), "Not meeting basic standard", mine.basic, { vote: -1, basic: !mine.basic }));
    if (data.reveal && blind(byId[selected])) {
      const id = selected;
      const revealOne = el("button", "ghost", "Reveal model");
      revealOne.disabled = revealing;
      revealOne.onclick = () => reveal([id]);
      bar.append(revealOne);
    }
    slot.replaceChildren(bar);
    if (!window.vellery.me) slot.append(el("span", "note", "Log in to vote"));
  }

  // While the viewer is open the grid stays put; it reorders when the viewer closes.
  function render() {
    if (!viewer.open) place();
    refresh();
    paintVotes();
    paintStatus();
    paintHeader();
    paintReveal();
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
    if (meta[id]) return;
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
    body.innerHTML = data.detail[id];
    const head = body.querySelector(".dhead");
    if (data.mode === "gallery") head.append(el("span", "verdict status"));
    if (data.votable[id]) head.after(el("div", "votes"));
    viewer.querySelector(".vpos").textContent = `${order.indexOf(byId[id]) + 1} of ${order.length}`;
    viewer.querySelector(".vpanel").scrollTop = 0;
    if (!viewer.open) viewer.showModal();
    byId[id].scrollIntoView({ block: "nearest" });
    refresh();
    paintVotes();
    paintStatus();
    paintHeader();
  }

  function open(id) {
    order = [...document.querySelectorAll(".tile")].filter((t) => !t.hidden);
    document.documentElement.classList.add("locked");
    show(id);
  }

  function step(by) {
    const at = order.indexOf(byId[selected]);
    show(order[(at + by + order.length) % order.length].dataset.id);
  }

  viewer.addEventListener("close", () => {
    document.documentElement.classList.remove("locked");
    const tile = byId[selected];
    selected = null;
    place();
    refresh();
    if (tile) tile.scrollIntoView({ block: "nearest" });
  });
  // Only a click on the empty space around the panel closes it. (Buttons inside get
  // rebuilt while handling their own click, so they can't be tested with `closest`.)
  viewer.addEventListener("click", (e) => {
    if (e.target === viewer || e.target.classList.contains("vwrap")) viewer.close();
  });
  viewer.querySelector(".vclose").addEventListener("click", () => viewer.close());
  viewer.querySelector(".prev").addEventListener("click", () => step(-1));
  viewer.querySelector(".next").addEventListener("click", () => step(1));
  viewer.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") step(-1);
    else if (e.key === "ArrowRight") step(1);
  });

  function pick(next) {
    variant = next;
    prompts.forEach((p) => p.classList.toggle("on", p.dataset.variant === variant));
    place();
    refresh();
    paintReveal();
  }

  async function load() {
    try {
      const res = await fetch(`/api/votes?task=${data.slug}`);
      if (res.ok) {
        votes = await res.json();
        for (const [id, v] of Object.entries(votes)) {
          if (v.revealed) meta[id] = v.revealed;
        }
        if (data.reveal) buildRows();
      }
    } catch {}
    remember();
    render();
  }

  prompts.forEach((p) => p.addEventListener("click", () => pick(p.dataset.variant)));
  tiles.forEach((t) => t.addEventListener("click", () => open(t.dataset.id)));
  document.addEventListener("vellery:auth", load);

  const revealButton = document.getElementById("reveal");
  if (revealButton) revealButton.addEventListener("click", () => reveal(blindTiles(variant).map((t) => t.dataset.id)));
  if (data.reveal) {
    document.getElementById("rate").onclick = () => {
      const available = [...board.querySelectorAll(".tile")].filter((t) => !t.hidden && blind(t));
      const next = available.find((t) => !tally(t.dataset.id).mine) || available[0];
      if (next) open(next.dataset.id);
    };
    try {
      const stored = localStorage.getItem(exposureKey);
      if (stored) meta = JSON.parse(stored);
      else {
        // Both older formats could carry a category reveal into newly added
        // drawings. Only the original gallery can inherit that decision.
        const previous = JSON.parse(localStorage.getItem(`vellery.disclosed.${data.slug}`) || "{}");
        const flags = (document.cookie.match(new RegExp(`${flagKey}=([a-z,]*)`)) || [])[1]?.split(",") || [];
        const snapshot = JSON.parse(localStorage.getItem(metaKey) || "{}");
        for (const id of data.legacyRevealIds || []) {
          const identity = previous[id] || (flags.includes(byId[id]?.dataset.variant) && snapshot[id]);
          if (identity) meta[id] = identity;
        }
        localStorage.setItem(exposureKey, JSON.stringify(meta));
      }
      localStorage.removeItem(`vellery.disclosed.${data.slug}`);
      localStorage.removeItem(metaKey);
      document.cookie = `${flagKey}=; Path=/; Max-Age=0; SameSite=Lax`;
    } catch {}
    window.addEventListener("storage", (e) => {
      if (e.key !== exposureKey || !e.newValue) return;
      Object.assign(meta, JSON.parse(e.newValue));
      buildRows();
      render();
    });
    buildRows();
  }
  place();
  pick("strong");
  load();
  window.vellery.ready.then(() => {
    paintVotes();
    paintReveal();
  });
})();

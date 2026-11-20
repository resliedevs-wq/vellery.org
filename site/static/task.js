// Task pages. Two modes:
//   scripted  one row per model, each cell opens that run in the viewer
//   gallery   drawings rated blind by visitors; models revealed on request
(() => {
  const data = JSON.parse(document.getElementById("data").textContent);
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };

  // ---------- the viewer, shared by both modes ----------
  const viewer = el("dialog", "viewer");
  viewer.innerHTML =
    '<div class="vframe"><div class="vtop"><span class="vpos"></span><span class="vkeys"></span>' +
    '<span class="vnavs"><button class="vbtn prev" aria-label="Previous (left arrow)">←</button>' +
    '<button class="vbtn next" aria-label="Next (right arrow)">→</button>' +
    '<button class="vbtn close" aria-label="Close (Esc)">✕</button></span></div>' +
    '<div class="vbody"></div></div>';
  document.body.append(viewer);
  const vbody = $(".vbody", viewer);
  vbody.tabIndex = -1;
  let order = [];
  let current = null;
  let onShow = () => {};

  function openViewer(list, id) {
    order = list;
    document.documentElement.classList.add("locked");
    show(id);
    if (!viewer.open) {
      viewer.showModal();
      vbody.focus({ preventScroll: true });
    }
  }
  function show(id) {
    current = id;
    $(".vpos", viewer).textContent = `${order.indexOf(id) + 1} of ${order.length}`;
    onShow(id);
    vbody.scrollTop = 0;
    viewer.querySelector(".vframe").scrollTop = 0;
  }
  function step(by) {
    if (!current || order.length < 2) return;
    const at = order.indexOf(current);
    show(order[(at + by + order.length) % order.length]);
  }
  viewer.addEventListener("close", () => {
    document.documentElement.classList.remove("locked");
    const id = current;
    current = null;
    document.dispatchEvent(new CustomEvent("viewer:closed", { detail: id }));
  });
  viewer.addEventListener("click", (e) => {
    if (e.target === viewer) viewer.close();
  });
  $(".close", viewer).onclick = () => viewer.close();
  $(".prev", viewer).onclick = () => step(-1);
  $(".next", viewer).onclick = () => step(1);
  const keyHandlers = [];
  document.addEventListener("keydown", (e) => {
    if (!viewer.open || !current || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.target.closest?.("input, textarea, select")) return;
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      e.preventDefault();
      step(e.key === "ArrowLeft" ? -1 : 1);
      return;
    }
    for (const h of keyHandlers) if (h(e)) return;
  });

  if (data.mode === "scripted") return scripted();
  return gallery();

  // ---------- scripted tasks ----------
  function scripted() {
    const cells = $$(".cell");
    $(".vkeys", viewer).textContent = "← → to step through runs";
    onShow = (id) => {
      vbody.innerHTML = data.detail[id];
      cells.forEach((c) => c.classList.toggle("on", c.dataset.id === id));
    };
    cells.forEach((c) => c.addEventListener("click", () => openViewer(cells.map((x) => x.dataset.id), c.dataset.id)));
    document.addEventListener("viewer:closed", (e) => {
      const cell = cells.find((c) => c.dataset.id === e.detail);
      cells.forEach((c) => c.classList.remove("on"));
      if (cell) cell.focus({ preventScroll: true });
    });
  }

  // ---------- drawings ----------
  function gallery() {
    const rules = data.rules;
    const tiles = $$(".shot");
    const byId = Object.fromEntries(tiles.map((t) => [t.dataset.id, t]));
    const grid = $("#grid");
    const blindBox = $("#blind");
    const revealedBox = $("#revealed");
    const byModel = $("#byModel");
    const exposureKey = `vellery.disclosed.v2.${data.slug}`;
    const cacheKey = `vellery.votes.${data.slug}`;
    const OPTIONS = [
      ["good", "Usable", "I could use this as is", { vote: 1, basic: false }],
      ["fix", "Needs fixing", "Close, but something is off", { vote: -1, basic: false }],
      ["slop", "Unusable", "Misses the request", { vote: -1, basic: true }],
    ];
    let variant = new URLSearchParams(location.search).get("prompt") === "vague" ? "weak" : "strong";
    if (data.variants && !data.variants.includes(variant)) variant = data.variants[0];
    let votes = {};
    let meta = {};
    // The site owner's rating is a drawing's verdict; see site/worker.js.
    let isOwner = false;
    let ratingRun = false;
    let revealing = false;
    const pending = {};
    const failed = {};

    try {
      meta = JSON.parse(localStorage.getItem(exposureKey) || "{}");
      for (const [id, v] of Object.entries(JSON.parse(localStorage.getItem(cacheKey) || "{}"))) votes[id] = { ...v, mine: null };
      isOwner = localStorage.getItem("vellery.owner") === "1";
    } catch {}
    const remember = () => {
      try {
        localStorage.setItem(exposureKey, JSON.stringify(meta));
        localStorage.setItem(cacheKey, JSON.stringify(Object.fromEntries(
          Object.entries(votes).map(([id, v]) => [id, { up: v.up, down: v.down, basic: v.basic, owner: v.owner }]))));
        localStorage.setItem("vellery.owner", isOwner ? "1" : "0");
      } catch {}
    };

    // A fresh random order on every visit, so no drawing always comes first.
    const shuffled = [...tiles];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    shuffled.forEach((t) => grid.append(t));

    const tally = (id) => votes[id] || { up: 0, down: 0, basic: 0, mine: null, owner: null };
    const blind = (id) => !meta[id];
    const gradeOf = (m) => (!m ? null : m.vote === 1 ? "good" : m.basic ? "slop" : "fix");
    // An owner's rating from any of their browsers counts as theirs.
    const mineOf = (id) => gradeOf(tally(id).mine || (isOwner ? tally(id).owner : null));
    const canRate = (id) => blind(id) || isOwner;
    function verdict(id) {
      const v = tally(id);
      if (v.owner) return gradeOf(v.owner);
      const total = v.up + v.down;
      if (total < rules.min) return null;
      if (v.up / total >= rules.green) return "good";
      if (v.up / total < rules.red && v.basic > v.down - v.basic) return "slop";
      return "fix";
    }
    const inVariant = (t) => t.dataset.variant === variant;

    // ----- page -----
    function renderTabs() {
      $$(".seg [role=tab]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.variant === variant)));
      $$(".pcard").forEach((c) => c.classList.toggle("on", c.dataset.variant === variant));
    }

    function renderCrowd() {
      for (const v of ["weak", "strong"]) {
        const ids = tiles.filter((t) => t.dataset.variant === v).map((t) => t.dataset.id);
        const c = { good: 0, fix: 0, slop: 0 };
        ids.forEach((id) => {
          const b = verdict(id);
          if (b) c[b]++;
        });
        const graded = c.good + c.fix + c.slop;
        const big = $(`[data-crowd="${v}"] b`);
        if (big) big.textContent = graded ? `${Math.round((100 * c.good) / graded)}%` : "–";
        const stack = $(`[data-crowd-stack="${v}"]`);
        if (stack) stack.replaceChildren(...Object.entries(c).filter(([, n]) => n).map(([g, n]) => {
          const s = el("span", g);
          s.style.width = `${(100 * n) / graded}%`;
          s.title = `${n} ${data.grades[g].toLowerCase()}`;
          return s;
        }));
        const note = $(`[data-crowd-note="${v}"]`);
        if (note) note.textContent = graded
          ? `${graded} of ${ids.length} drawings rated`
          : `${ids.length} drawings · none rated yet`;
      }
    }

    function paintTile(t) {
      const id = t.dataset.id;
      const cap = $(".cap", t);
      const mine = mineOf(id);
      t.classList.toggle("on", id === current);
      if (blind(id)) {
        t.dataset.g = "";
        t.dataset.mine = mine || "";
        cap.textContent = mine ? `You: ${data.grades[mine]}` : "";
        t.setAttribute("aria-label", `Drawing ${data.detail[id].kid}${mine ? `, you rated it ${data.grades[mine]}` : ", not rated yet"}`);
      } else {
        const who = meta[id];
        const g = verdict(id);
        t.dataset.g = g || "";
        t.dataset.mine = "";
        cap.replaceChildren(el("b", "", g ? data.grades[g] : "Not rated yet"), el("span", "", `Run ${who.run}`));
        t.setAttribute("aria-label", `${who.label}, run ${who.run}${g ? `: ${data.grades[g]}` : ""}`);
      }
    }

    function place() {
      // Blind drawings stay in the shuffled grid; revealed ones move to their model's row.
      const revealed = tiles.filter((t) => !blind(t.dataset.id));
      for (const m of data.models) {
        const mine = revealed.filter((t) => meta[t.dataset.id].id === m.id).sort((a, b) => meta[a.dataset.id].run - meta[b.dataset.id].run);
        if (!mine.length) continue;
        let row = $(`.mrow[data-model="${m.id}"]`, byModel);
        if (!row) {
          row = el("div", "mrow");
          row.dataset.model = m.id;
          row.append(el("div", "mlabel"), el("div", "mtiles"));
          $(".mlabel", row).append(el("b", "", m.label), el("span", "mscore"));
          byModel.append(row);
          [...byModel.children]
            .sort((a, b) => data.models.findIndex((x) => x.id === a.dataset.model) - data.models.findIndex((x) => x.id === b.dataset.model))
            .forEach((r) => byModel.append(r));
        }
        mine.forEach((t) => $(".mtiles", row).append(t));
      }
    }

    function render() {
      renderTabs();
      tiles.forEach((t) => {
        t.hidden = !inVariant(t);
        paintTile(t);
      });
      const here = tiles.filter(inVariant);
      const blindHere = here.filter((t) => blind(t.dataset.id));
      const rated = here.filter((t) => mineOf(t.dataset.id)).length;
      blindBox.hidden = !blindHere.length;
      $(".count", blindBox).textContent = blindHere.length;
      const revealedHere = here.length - blindHere.length;
      revealedBox.hidden = !revealedHere;
      $(".count", revealedBox).textContent = revealedHere;
      $$(".mrow", byModel).forEach((row) => {
        const ts = $$(".shot", row).filter(inVariant);
        row.hidden = !ts.length;
        const good = ts.filter((t) => verdict(t.dataset.id) === "good").length;
        const judged = ts.filter((t) => verdict(t.dataset.id)).length;
        $(".mscore", row).textContent = judged ? `${good} of ${judged} rated usable` : "not rated yet";
      });
      $("#progress").textContent = rated
        ? `You’ve rated ${rated} of ${here.length}`
        : `${here.length} drawings, none rated by you yet`;
      $("#pbar").style.width = `${(100 * rated) / (here.length || 1)}%`;
      const unratedBlind = blindHere.filter((t) => !mineOf(t.dataset.id));
      const rate = $("#rate");
      rate.disabled = !unratedBlind.length;
      rate.textContent = !blindHere.length ? "All revealed" : !unratedBlind.length ? "All rated" : rated ? "Continue rating" : "Start rating";
      const reveal = $("#reveal");
      if (reveal) {
        reveal.hidden = !blindHere.length;
        reveal.disabled = revealing || blindHere.some((t) => pending[t.dataset.id]);
        reveal.textContent = unratedBlind.length ? "Reveal all models" : "Reveal models";
      }
      renderCrowd();
      if (viewer.open && current) paintSide();
    }

    // ----- viewer -----
    $(".vkeys", viewer).textContent = "1 2 3 to rate · ← → to step through";
    const visibleOrder = () => [
      ...$$(".shot", grid).filter((t) => !t.hidden),
      ...$$(".shot", byModel).filter((t) => !t.hidden),
    ].map((t) => t.dataset.id);

    onShow = (id) => {
      const d = data.detail[id];
      vbody.innerHTML =
        `<div class="vgal"><div class="vart">${d.html}</div><aside class="vside">` +
        '<p class="crumb"></p><h2></h2><p class="whohint"></p><div class="rate" role="group" aria-label="Your rating"></div>' +
        '<p class="status" aria-live="polite"></p><div class="after"></div></aside></div>';
      tiles.forEach(paintTile);
      paintSide();
      byId[id].scrollIntoView({ block: "nearest" });
    };

    function paintSide() {
      const id = current;
      const side = $(".vside", vbody);
      if (!side) return;
      const d = data.detail[id];
      const who = meta[id];
      const mine = mineOf(id);
      $(".crumb", side).textContent = `${d.variant === "weak" ? "Vague" : "Specific"} prompt · drawing ${d.kid}`;
      $("h2", side).textContent = who ? who.label : "Who drew this?";
      $(".whohint", side).textContent = who ? `Run ${who.run} of 5` : "Rate it first. The model stays hidden until you reveal it.";
      const rate = $(".rate", side);
      if (who && !isOwner) {
        const v = tally(id);
        const g = verdict(id);
        const fix = v.down - v.basic;
        rate.replaceChildren();
        const box = el("div", "crowd");
        box.append(
          el("p", "label", v.owner ? "Vellery’s rating" : "Visitor ratings"),
          el("p", `crowdverdict ${g || ""}`, g ? data.grades[g] : "Not rated yet"),
        );
        if (v.owner) box.append(el("p", "label", "Visitor ratings"));
        const ul = el("ul", "breakdown");
        [["good", v.up], ["fix", fix], ["slop", v.basic]].forEach(([k, n]) => {
          const li = el("li", k);
          li.append(el("b", "", String(n)), document.createTextNode(` ${data.grades[k].toLowerCase()}`));
          ul.append(li);
        });
        box.append(ul);
        if (mine) box.append(el("p", "hint", `You rated it ${data.grades[mine].toLowerCase()}.`));
        else box.append(el("p", "hint", "Rating is closed for you on this drawing because you revealed its model."));
        rate.append(box);
      } else {
        const focused = rate.contains(document.activeElement) ? document.activeElement.dataset.g : null;
        rate.replaceChildren(...OPTIONS.map(([g, label, hint, next], n) => {
          const b = el("button", `opt ${g}${mine === g ? " on" : ""}`);
          b.dataset.g = g;
          b.setAttribute("aria-pressed", String(mine === g));
          b.append(el("kbd", "", String(n + 1)), el("b", "", label), el("span", "", hint));
          b.onclick = () => vote(id, mine === g ? null : next);
          return b;
        }));
        if (focused) $(`[data-g="${focused}"]`, rate)?.focus({ preventScroll: true });
      }
      const status = $(".status", side);
      status.textContent = failed[id] ? "Couldn’t save that rating. Try again." : pending[id] ? "Saving…"
        : mine && canRate(id) ? (isOwner ? "Saved as Vellery’s rating" : "Saved") : "";
      status.classList.toggle("err", !!failed[id]);
      const after = $(".after", side);
      after.replaceChildren();
      const next = nextUnrated(id);
      if (!who && data.reveal) {
        const r = el("button", "btn", "Reveal the model");
        r.disabled = revealing || !!pending[id];
        r.title = mine ? "" : "Revealing ends rating for this drawing";
        r.onclick = () => reveal([id]);
        after.append(r);
      }
      if (next) {
        const n = el("button", "btn primary", "Next unrated →");
        n.onclick = () => { ratingRun = true; show(next); };
        after.append(n);
      }
    }

    function nextUnrated(from) {
      const list = $$(".shot", grid).filter((t) => !t.hidden).map((t) => t.dataset.id);
      const start = Math.max(0, list.indexOf(from));
      for (let k = 1; k <= list.length; k++) {
        const id = list[(start + k) % list.length];
        if (id !== from && !mineOf(id) && blind(id)) return id;
      }
      return null;
    }

    keyHandlers.push((e) => {
      const n = ["1", "2", "3"].indexOf(e.key);
      if (n < 0 || !canRate(current)) return false;
      e.preventDefault();
      if (e.repeat) return true;
      const [g, , , next] = OPTIONS[n];
      vote(current, mineOf(current) === g ? null : next);
      return true;
    });

    // ----- votes -----
    function applyLocal(v, next) {
      // Owner votes stay out of the visitor tallies.
      if (isOwner) return { ...v, mine: next, owner: next };
      const out = { ...v, mine: next };
      if (v.mine) {
        if (v.mine.vote === 1) out.up--;
        else { out.down--; if (v.mine.basic) out.basic--; }
      }
      if (next) {
        if (next.vote === 1) out.up++;
        else { out.down++; if (next.basic) out.basic++; }
      }
      return out;
    }

    // The page updates at once; writes for one drawing go out in order, and a
    // failed save puts the last confirmed state back.
    async function vote(id, next) {
      if (!canRate(id)) return;
      const wasUnrated = !mineOf(id);
      const before = tally(id);
      votes[id] = applyLocal(before, next);
      delete failed[id];
      if (ratingRun && wasUnrated && next) {
        const after = nextUnrated(id);
        if (after) setTimeout(() => { if (current === id) show(after); }, 380);
      }
      if (pending[id]) {
        pending[id].next = next;
        render();
        return;
      }
      const state = (pending[id] = { next });
      let confirmed = before;
      render();
      while (true) {
        const sending = state.next;
        try {
          const res = await fetch("/api/vote", {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({ item: id, vote: sending?.vote || 0, basic: !!sending?.basic }),
          });
          if (!res.ok) throw new Error(res.status);
          confirmed = await res.json();
        } catch {
          failed[id] = true;
          break;
        }
        if (state.next === sending) break;
      }
      delete pending[id];
      votes[id] = confirmed;
      remember();
      render();
    }

    async function reveal(ids) {
      if (revealing || !ids.length || ids.some((id) => pending[id])) return;
      const unrated = ids.filter((id) => !mineOf(id)).length;
      if (unrated && !isOwner) {
        const what = ids.length === 1 ? "You haven’t rated this drawing. Revealing its model ends rating for it."
          : `You haven’t rated ${unrated} of these ${ids.length} drawings. Revealing their models ends rating for them.`;
        if (!window.confirm(`${what} Reveal anyway?`)) return;
      }
      revealing = true;
      render();
      try {
        const res = await fetch("/api/reveal", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ task: data.slug, ids }),
        });
        if (!res.ok) throw new Error();
        const disclosed = await res.json();
        if (!ids.every((id) => disclosed[id])) throw new Error();
        Object.assign(meta, disclosed);
        remember();
        place();
      } catch {
        window.alert("Could not reveal the models. Please try again.");
      } finally {
        revealing = false;
        render();
      }
    }

    async function load() {
      try {
        const res = await fetch(`/api/votes?task=${encodeURIComponent(data.slug)}`);
        if (res.ok) {
          const { items: received, owner } = await res.json();
          isOwner = owner;
          for (const id of Object.keys(pending)) received[id] = votes[id];
          votes = received;
          for (const [id, v] of Object.entries(votes)) if (v.revealed) meta[id] = v.revealed;
          remember();
        }
      } catch {}
      place();
      render();
    }

    // ----- wiring -----
    tiles.forEach((t) => t.addEventListener("click", () => {
      ratingRun = false;
      openViewer(visibleOrder(), t.dataset.id);
    }));
    $$(".seg [role=tab]").forEach((b) => b.addEventListener("click", () => {
      variant = b.dataset.variant;
      const url = new URL(location.href);
      url.searchParams.set("prompt", variant === "weak" ? "vague" : "specific");
      history.replaceState(null, "", url);
      render();
    }));
    $("#rate").onclick = () => {
      const first = $$(".shot", grid).find((t) => !t.hidden && !mineOf(t.dataset.id));
      if (!first) return;
      ratingRun = true;
      openViewer(visibleOrder(), first.dataset.id);
    };
    const revealAll = $("#reveal");
    if (revealAll) revealAll.onclick = () => reveal(tiles.filter((t) => inVariant(t) && blind(t.dataset.id)).map((t) => t.dataset.id));
    document.addEventListener("viewer:closed", (e) => {
      ratingRun = false;
      render();
      const t = byId[e.detail];
      if (t && !t.hidden) t.focus({ preventScroll: true });
    });
    window.addEventListener("storage", (e) => {
      if (e.key !== exposureKey || !e.newValue) return;
      try { Object.assign(meta, JSON.parse(e.newValue)); } catch {}
      place();
      render();
    });

    place();
    render();
    load();
  }
})();

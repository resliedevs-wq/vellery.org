(() => {
  const { slug, grades, items, prompts } = JSON.parse(document.getElementById("data").textContent);
  const $ = (id) => document.getElementById(id);
  const votes = JSON.parse(localStorage.getItem("vellery.votes") || "{}");
  let voter = localStorage.getItem("vellery.voter");
  if (!voter) {
    voter = [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, "0")).join("");
    localStorage.setItem("vellery.voter", voter);
  }

  // Same order every visit for one voter, different between voters.
  let h = 0;
  for (const c of voter) h = (Math.imul(h, 31) + c.charCodeAt(0)) | 0;
  const rand = () => {
    h = (h + 0x6d2b79f5) | 0;
    let t = Math.imul(h ^ (h >>> 15), 1 | h);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const order = items.slice();
  for (let i = order.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [order[i], order[j]] = [order[j], order[i]];
  }
  const queue = order.filter((i) => !votes[i.id]).concat(order.filter((i) => votes[i.id]));
  let at = Math.max(0, queue.findIndex((i) => i.id === location.hash.slice(1)));

  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };

  function renderItem(it) {
    const box = $("item");
    box.replaceChildren();
    if (it.kind === "image") {
      it.srcs.forEach((s) => {
        const img = el("img");
        img.src = s;
        box.append(img);
      });
    } else if (it.kind === "sheet") {
      const wrap = el("div", "sheet");
      if (it.rows) {
        const table = el("table");
        it.rows.forEach((row, n) => {
          const tr = el("tr");
          row.forEach((cell) => tr.append(el(n ? "td" : "th", "", cell)));
          table.append(tr);
        });
        wrap.append(table);
      }
      if (it.text) wrap.append(el("pre", "", it.text));
      box.append(wrap);
    } else {
      box.append(el("pre", "doc", it.text));
    }
  }

  function showTally(t) {
    const total = Object.values(t).reduce((a, b) => a + b, 0) || 1;
    $("result").replaceChildren(
      ...Object.entries(grades).map(([g, label]) => {
        const row = el("div", "bar");
        const bar = el("i");
        const fill = el("s");
        fill.style.width = `${(100 * (t[g] || 0)) / total}%`;
        fill.style.background = `var(--${g})`;
        bar.append(fill);
        row.append(el("span", "", label), bar, el("span", "num", String(t[g] || 0)));
        return row;
      }),
    );
  }

  function render() {
    const it = queue[at];
    $("progress").textContent = `${at + 1} of ${queue.length} · ${Object.keys(votes).filter((k) => k.startsWith(slug + ".")).length} rated`;
    $("prompt").textContent = prompts[it.variant];
    $("variant").textContent = `${it.variant[0].toUpperCase()}${it.variant.slice(1)} prompt`;
    renderItem(it);
    $("result").replaceChildren();
    $("buttons").replaceChildren(
      ...Object.entries(grades).map(([g, label], n) => {
        const b = el("button", `choice ${g}` + (votes[it.id] === g ? " on" : ""), label);
        b.title = `Key ${n + 1}`;
        b.addEventListener("click", () => rate(it, g));
        return b;
      }),
      Object.assign(el("button", "choice next", "Next →"), { onclick: next }),
    );
    history.replaceState(null, "", `#${it.id}`);
  }

  async function rate(it, g) {
    try {
      const res = await fetch("/api/rate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ item: it.id, rating: g, voter }),
      });
      if (!res.ok) throw new Error(res.status);
      votes[it.id] = g;
      localStorage.setItem("vellery.votes", JSON.stringify(votes));
      render();
      showTally(await res.json());
    } catch {
      $("result").replaceChildren(el("span", "", "Couldn't save that. Try again."));
    }
  }

  function next() {
    at = (at + 1) % queue.length;
    render();
  }

  document.addEventListener("keydown", (e) => {
    const g = Object.keys(grades)[Number(e.key) - 1];
    if (g) rate(queue[at], g);
    else if (e.key === "ArrowRight") next();
  });
  render();
})();

// Home page: fill in drawing verdicts from /api/summary (the Worker holds
// which model drew what), add them to each model's usable total, and re-sort.
(() => {
  const GRADES = { good: "usable", fix: "needs fixing", slop: "unusable" };
  const el = (tag, cls) => Object.assign(document.createElement(tag), cls ? { className: cls } : {});

  function fill(summary) {
    // Task rows: one stacked bar per drawing task.
    document.querySelectorAll("[data-summary]").forEach((box) => {
      const all = Object.values(summary[box.dataset.summary] || {}).flat();
      const c = { good: 0, fix: 0, slop: 0 };
      all.forEach((g) => g && c[g]++);
      const rated = c.good + c.fix + c.slop;
      box.querySelector(".stack").replaceChildren(...Object.entries(c).filter(([, n]) => n).map(([g, n]) => {
        const s = el("span", g);
        s.style.width = `${(100 * n) / rated}%`;
        s.title = `${n} ${GRADES[g]}`;
        return s;
      }));
      box.querySelector("b").textContent = rated ? `${Math.round((100 * c.good) / rated)}%` : "–";
      box.querySelector(".sumnote").textContent = rated
        ? `share of drawings rated usable${rated < all.length ? ` · ${rated} of ${all.length} rated` : ""}`
        : "no drawings rated yet";
    });

    // Models table: drawing dots, then points.
    rows().forEach((row) => {
      let points = +row.dataset.points;
      let max = +row.dataset.max;
      const missing = row.dataset.missing ? row.dataset.missing.split(" · ") : [];
      row.querySelectorAll("[data-draw]").forEach((cell) => {
        const runs = (summary[cell.dataset.draw] || {})[row.dataset.model] || [];
        const dots = cell.querySelector(".dots");
        dots.replaceChildren(...runs.map((g) => el("i", g || "")));
        if (!runs.length) dots.textContent = "–";
        const ok = runs.filter((g) => g === "good").length;
        const rated = runs.filter(Boolean);
        dots.title = runs.length ? `${ok} of ${runs.length} rated usable${rated.length < runs.length ? `, ${runs.length - rated.length} not rated yet` : ""}` : "Not run on this task";
        points += rated.reduce((sum, g) => sum + POINTS[g], 0);
        max += 2 * rated.length;
        if (runs.length < +cell.dataset.expect) missing.push(cell.dataset.title);
      });
      row.dataset.score = points;
      row.dataset.out = missing.length ? "1" : "";
      row.querySelector(".points").innerHTML = `<b>${points}</b>`;
      row.querySelector(".points").title = `${points} of ${max} points`;
      row.querySelector("th").title = missing.length ? `Not ranked: not run on ${missing.join(", ")}` : "";
    });
    rank();
  }

  const POINTS = { good: 2, fix: 1, slop: 0 };
  const body = document.querySelector("table.models tbody");
  const rows = () => (body ? [...body.querySelectorAll("tr[data-model]")] : []);
  let by = "points";

  // Ranked models first, then the ones that didn't run every task.
  function rank() {
    if (!body) return;
    const score = (r) => +(r.dataset.score ?? r.dataset.points);
    const cost = (r) => +r.dataset.cost;
    const cmp = by === "cost"
      ? (a, b) => cost(a) - cost(b) || score(b) - score(a)
      : (a, b) => score(b) - score(a) || cost(a) - cost(b);
    const all = rows().sort((a, b) => cmp(a, b) || a.dataset.order - b.dataset.order);
    const ranked = all.filter((r) => !r.dataset.out);
    const out = all.filter((r) => r.dataset.out);
    body.querySelector(".divider")?.remove();
    let n = 0, prev = null;
    ranked.forEach((r, i) => {
      const key = by === "cost" ? cost(r) : score(r);
      if (key !== prev) n = i + 1;
      prev = key;
      r.querySelector(".rank").textContent = n;
      body.append(r);
    });
    if (out.length) {
      const d = el("tr", "divider");
      const td = el("td");
      td.colSpan = all[0].cells.length;
      td.append(Object.assign(el("span"), { textContent: "Not ranked · not run on every task" }));
      d.append(td);
      body.append(d);
    }
    out.forEach((r) => {
      r.querySelector(".rank").textContent = "";
      r.classList.add("unranked");
      body.append(r);
    });
    document.querySelectorAll("[data-rank]").forEach((b) => {
      if (b.tagName === "BUTTON") b.setAttribute("aria-pressed", String(b.dataset.rank === by));
      else b.classList.toggle("sorted", b.dataset.rank === by);
    });
  }

  document.querySelectorAll("[data-rank]").forEach((b) => b.addEventListener("click", () => {
    by = b.dataset.rank;
    rank();
  }));
  rank();

  fetch("/api/summary").then((r) => (r.ok ? r.json() : null)).then((s) => s && fill(s)).catch(() => {});
})();

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

    // Models table: dots per run, then totals and order.
    const body = document.querySelector("table.models tbody");
    if (!body) return;
    const rows = [...body.rows];
    rows.forEach((row) => {
      let good = +row.dataset.good;
      let n = +row.dataset.n;
      row.querySelectorAll("[data-draw]").forEach((cell) => {
        const runs = (summary[cell.dataset.draw] || {})[row.dataset.model] || [];
        const dots = cell.querySelector(".dots");
        dots.replaceChildren(...runs.map((g) => el("i", g || "")));
        if (!runs.length) dots.textContent = "–";
        const ok = runs.filter((g) => g === "good").length;
        const rated = runs.filter(Boolean).length;
        dots.title = runs.length ? `${ok} of ${runs.length} rated usable${rated < runs.length ? `, ${runs.length - rated} not rated yet` : ""}` : "Not run on this task";
        good += ok;
        n += rated;
      });
      row.querySelector(".usable").innerHTML = `<b>${good}</b>/${n}`;
      row.dataset.share = n ? good / n : 0;
    });
    // Models weren't all run on every task, so rank by share, not count.
    rows.sort((a, b) => b.dataset.share - a.dataset.share || a.dataset.order - b.dataset.order)
      .forEach((r) => body.append(r));
  }

  fetch("/api/summary").then((r) => (r.ok ? r.json() : null)).then((s) => s && fill(s)).catch(() => {});
})();

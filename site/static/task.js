(() => {
  const data = JSON.parse(document.getElementById("data").textContent);
  const prompts = [...document.querySelectorAll(".prompt")];
  const detail = document.getElementById("detail");
  const colors = { good: "var(--good)", fix: "var(--fix)", slop: "var(--slop)" };
  let tally = {};

  function tallyText(t) {
    if (!t) return "";
    const parts = Object.entries(data.grades).filter(([g]) => t[g]).map(([g, label]) => `${t[g]} ${label.toLowerCase()}`);
    return parts.length ? `Visitors rated it: ${parts.join(", ")}` : "";
  }

  function show(cell) {
    document.querySelectorAll(".cell.on").forEach((c) => c.classList.remove("on"));
    cell.classList.add("on");
    detail.innerHTML = data.detail[cell.dataset.id];
    const text = tallyText(tally[cell.dataset.id]);
    if (text) {
      const p = document.createElement("p");
      p.className = "note";
      p.textContent = text;
      detail.querySelector(".dhead > div").append(p);
    }
    detail.hidden = false;
  }

  function pick(variant) {
    prompts.forEach((p) => p.classList.toggle("on", p.dataset.variant === variant));
    if (data.mode === "gallery") {
      document.getElementById("gallery").dataset.variant = variant;
      return;
    }
    document.querySelectorAll(".grid").forEach((g) => (g.hidden = g.dataset.variant !== variant));
    const grid = document.querySelector(`.grid[data-variant="${variant}"]`);
    show(grid.querySelector(".cell:not(.good)") || grid.querySelector(".cell"));
  }

  prompts.forEach((p) => p.addEventListener("click", () => pick(p.dataset.variant)));
  document.querySelectorAll(".cell").forEach((c) =>
    c.addEventListener("click", () => {
      show(c);
      if (detail.getBoundingClientRect().top > innerHeight * 0.8) detail.scrollIntoView({ behavior: "smooth", block: "start" });
    }),
  );
  pick("strong");

  fetch(`/api/ratings?task=${data.slug}`)
    .then((r) => (r.ok ? r.json() : {}))
    .then((t) => {
      tally = t;
      document.querySelectorAll(".shot").forEach((s) => {
        const box = s.querySelector(".tally");
        for (const [g, n] of Object.entries(t[s.dataset.id] || {}))
          for (let i = 0; i < n; i++) {
            const dot = document.createElement("i");
            dot.style.background = colors[g];
            box.append(dot);
          }
      });
      const on = document.querySelector(".cell.on");
      if (on) show(on);
    })
    .catch(() => {});
})();

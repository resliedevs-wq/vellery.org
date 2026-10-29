(() => {
  const data = JSON.parse(document.getElementById("data").textContent);
  const prompts = [...document.querySelectorAll(".prompt")];
  const detail = document.getElementById("detail");
  const colors = { good: "var(--good)", fix: "var(--fix)", slop: "var(--slop)" };
  let tally = {};

  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };

  function tallyText(t) {
    if (!t) return "";
    const parts = Object.entries(data.grades).filter(([g]) => t[g]).map(([g, label]) => `${t[g]} ${label.toLowerCase()}`);
    return parts.length ? `Visitors: ${parts.join(", ")}` : "";
  }

  function pick(variant) {
    prompts.forEach((p) => p.classList.toggle("on", p.dataset.variant === variant));
    if (data.mode === "gallery") {
      document.getElementById("gallery").dataset.variant = variant;
    } else {
      document.querySelectorAll(".grid").forEach((g) => (g.hidden = g.dataset.variant !== variant));
      detail.hidden = true;
      document.querySelectorAll(".cell.on").forEach((c) => c.classList.remove("on"));
    }
  }

  function show(id, cell) {
    const r = data.runs[id];
    document.querySelectorAll(".cell.on").forEach((c) => c.classList.remove("on"));
    cell.classList.add("on");
    detail.replaceChildren(el("h2", "", `${r.model} · run ${r.run}`));
    if (r.grade) detail.append(el("span", `chip ${r.grade}`, data.grades[r.grade] + (r.why ? ` · ${r.why}` : "")));
    detail.append(el("pre", "out", r.text));
    const meta = [tallyText(tally[id]), r.cost != null ? `$${r.cost.toFixed(4)} at API prices` : ""].filter(Boolean);
    if (meta.length) detail.append(el("p", "note", meta.join(" · ")));
    detail.hidden = false;
  }

  prompts.forEach((p) => p.addEventListener("click", () => pick(p.dataset.variant)));
  document.querySelectorAll(".cell").forEach((c) => c.addEventListener("click", () => show(c.dataset.id, c)));
  pick("strong");

  fetch(`/api/ratings?task=${data.slug}`)
    .then((r) => (r.ok ? r.json() : {}))
    .then((t) => {
      tally = t;
      document.querySelectorAll(".shot").forEach((s) => {
        const box = s.querySelector(".tally");
        for (const [g, n] of Object.entries(t[s.dataset.id] || {}))
          for (let i = 0; i < n; i++) {
            const dot = el("i");
            dot.style.background = colors[g];
            box.append(dot);
          }
      });
    })
    .catch(() => {});
})();

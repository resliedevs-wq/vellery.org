// Test-stage login: one shared account. Exposes window.vellery for task.js.
(() => {
  const slot = document.getElementById("auth");
  const state = { me: null };
  const dialog = document.createElement("dialog");
  dialog.className = "login";
  dialog.innerHTML =
    '<form method="dialog"><h2>Log in</h2>' +
    '<label>Username<input name="user" autocomplete="username" required></label>' +
    '<label>Password<input name="password" type="password" autocomplete="current-password" required></label>' +
    '<p class="note">Test stage: admin / password</p><p class="error" hidden></p>' +
    '<div class="actions"><button type="button" class="cancel">Cancel</button><button class="primary">Log in</button></div></form>';
  document.body.append(dialog);
  const form = dialog.querySelector("form");
  const error = dialog.querySelector(".error");
  dialog.querySelector(".cancel").addEventListener("click", () => dialog.close());

  function paint() {
    slot.replaceChildren();
    const b = document.createElement("button");
    b.className = "link";
    b.textContent = state.me ? "Log out" : "Log in";
    b.addEventListener("click", state.me ? logout : () => api.openLogin());
    if (state.me) {
      const who = document.createElement("span");
      who.textContent = state.me;
      slot.append(who);
    }
    slot.append(b);
  }

  function set(me) {
    state.me = me;
    api.me = me;
    paint();
    document.dispatchEvent(new CustomEvent("vellery:auth", { detail: me }));
  }

  async function logout() {
    await fetch("/api/logout", { method: "POST" });
    set(null);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    error.hidden = true;
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ user: form.user.value, password: form.password.value }),
    });
    if (!res.ok) {
      error.textContent = "Wrong username or password.";
      error.hidden = false;
      return;
    }
    form.reset();
    dialog.close();
    set((await res.json()).user);
  });

  const api = {
    me: null,
    openLogin: () => {
      error.hidden = true;
      dialog.showModal();
      form.user.focus();
    },
  };
  window.vellery = api;
  api.ready = fetch("/api/me")
    .then((r) => (r.ok ? r.json() : { user: null }))
    .catch(() => ({ user: null }))
    .then((m) => {
      state.me = m.user;
      api.me = m.user;
      paint();
    });
})();

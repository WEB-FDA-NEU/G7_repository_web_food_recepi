/**
 * <site-header> — a tiny custom element instead of copy-pasted markup in
 * every page. Reads the current file name to mark the active nav link, and
 * listens for auth:change (fired by auth.js) to swap the sign-in state.
 */
class SiteHeader extends HTMLElement {
  connectedCallback() {
    this.render();
    this.wireEvents();
    window.addEventListener("auth:change", () => this.render());
  }

  currentPage() {
    const path = window.location.pathname.split("/").pop() || "index.html";
    return path;
  }

  render() {
    const page = this.currentPage();
    const user = window.Auth ? window.Auth.getUser() : null;
    const link = (href, label) =>
      `<a href="${href}" ${page === href ? 'aria-current="page"' : ""}>${label}</a>`;

    const actions = user
      ? `
        <span class="eyebrow-plain">Hi, ${user.name}</span>
        <button class="btn btn--ghost btn--sm" data-action="sign-out" type="button">Sign out</button>
      `
      : `
        <a class="btn btn--ghost btn--sm" href="login.html">Sign in</a>
        <a class="btn btn--primary btn--sm" href="register.html">Share a recipe</a>
      `;

    this.innerHTML = `
      <div class="container site-header__bar">
        <a class="site-header__brand" href="index.html">
          <span class="site-header__brand-mark">◒</span> Ladle
        </a>
        <nav class="site-header__nav">
          <div class="site-header__links">
            ${link("index.html", "Home")}
            ${link("list.html", "Browse")}
          </div>
          <div class="site-header__actions">${actions}</div>
        </nav>
        <button class="site-header__toggle" type="button" aria-label="Toggle menu" data-action="toggle-menu">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18M3 12h18M3 18h18"/>
          </svg>
        </button>
      </div>
    `;
  }

  wireEvents() {
    this.addEventListener("click", (e) => {
      const action = e.target.closest("[data-action]")?.dataset.action;
      if (action === "toggle-menu") {
        this.closest(".site-header")?.classList.toggle("site-header--open");
      }
      if (action === "sign-out") {
        window.Auth.signOut();
        window.location.href = "index.html";
      }
    });
  }
}

customElements.define("site-header", SiteHeader);

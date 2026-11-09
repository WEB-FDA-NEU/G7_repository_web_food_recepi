/**
 * <site-footer> — static, but kept as a component so every page stays in
 * sync when a link changes here.
 */
class SiteFooter extends HTMLElement {
  connectedCallback() {
    this.render();
  }

  render() {
    const year = new Date().getFullYear();
    this.innerHTML = `
      <div class="container">
        <div class="site-footer__grid">
          <div>
            <p class="site-footer__brand">◒ Ladle</p>
            <p>Recipes worth writing down, shared by people who actually cook them.</p>
          </div>
          <div class="site-footer__cols">
            <div class="site-footer__col">
              <h3>Explore</h3>
              <a href="index.html">Home</a>
              <a href="list.html">Browse recipes</a>
            </div>
            <div class="site-footer__col">
              <h3>Account</h3>
              <a href="login.html">Sign in</a>
              <a href="register.html">Create account</a>
            </div>
          </div>
        </div>
        <div class="site-footer__base">
          <p>&copy; ${year} Ladle. A demo project — all recipes are for illustration.</p>
        </div>
      </div>
    `;
  }
}

customElements.define("site-footer", SiteFooter);

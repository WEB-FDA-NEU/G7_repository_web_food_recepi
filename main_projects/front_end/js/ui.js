/**
 * ui.js
 * The only file that touches the DOM's event listeners and decides what
 * happens on each page. Each page sets <body data-page="..."> so this one
 * script can be included everywhere and just run the matching init.
 */
(() => {
  function init() {
    const page = document.body.dataset.page;
    const initializers = {
      home: initHome,
      list: initList,
      detail: initDetail,
      login: initAuthForm,
      register: initAuthForm
    };
    initializers[page]?.();
  }

  async function initHome() {
    const grid = document.querySelector("#latest-grid");
    if (!grid) return;
    grid.innerHTML = Render.cardSkeletonGrid(3);
    try {
      const recipes = await Api.getRecipes();
      grid.innerHTML = Render.recipeCardList(recipes.slice(0, 6));
    } catch (err) {
      grid.innerHTML = `<div class="empty-state"><h3>Couldn't load recipes</h3><p class="lede">${Render.errorAlert(err.message)}</p></div>`;
    }
  }

  async function initList() {
    const grid = document.querySelector("#recipe-grid");
    const chipsEl = document.querySelector("#category-chips");
    const searchInput = document.querySelector("#search-input");
    const resultCount = document.querySelector("#result-count");
    const categories = window.APP_CONFIG.CATEGORIES;

    const params = new URLSearchParams(window.location.search);
    let activeCategory = params.get("category") || "all";
    let query = params.get("q") || "";
    if (searchInput) searchInput.value = query;

    chipsEl.innerHTML = Render.categoryChips(categories, activeCategory);

    async function load() {
      grid.innerHTML = Render.cardSkeletonGrid(6);
      try {
        const recipes = await Api.getRecipes({ category: activeCategory, query });
        grid.innerHTML = Render.recipeCardList(recipes);
        if (resultCount) {
          resultCount.textContent = `${recipes.length} recipe${recipes.length === 1 ? "" : "s"}`;
        }
      } catch (err) {
        grid.innerHTML = `<div class="empty-state"><h3>Something went wrong</h3><p class="lede">${Render.errorAlert(err.message)}</p></div>`;
      }
    }

    chipsEl.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-category]");
      if (!btn) return;
      activeCategory = btn.dataset.category;
      chipsEl.querySelectorAll(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c === btn)));
      load();
    });

    let debounceTimer;
    searchInput?.addEventListener("input", (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        query = e.target.value.trim();
        load();
      }, 250);
    });

    load();
  }

  async function initDetail() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id") || "1";

    const headerEl = document.querySelector("#detail-header");
    const ingredientsEl = document.querySelector("#ingredients-list");
    const stepsEl = document.querySelector("#steps-container");
    const notesEl = document.querySelector("#notes-container");
    const servingsValueEl = document.querySelector("#servings-value");
    const noteBlock = document.querySelector("#notes-block");

    try {
      const recipe = await Api.getRecipeById(id);
      const parts = Render.recipeDetail(recipe);

      headerEl.innerHTML = parts.header;
      ingredientsEl.innerHTML = parts.ingredients;
      stepsEl.innerHTML = parts.steps;
      document.title = `${recipe.title} — Ladle`;

      if (servingsValueEl) servingsValueEl.textContent = recipe.servings;
      if (parts.notes && noteBlock) {
        notesEl.innerHTML = parts.notes;
        noteBlock.hidden = false;
      }

      wireServingsStepper(recipe.servings);
      wireSaveButton(recipe);
    } catch (err) {
      headerEl.innerHTML = `<h1 class="h1">Recipe not found</h1><p class="lede">${Render.errorAlert(err.message)} Try browsing the full list instead.</p>`;
      document.querySelector("#detail-aside")?.remove();
    }
  }

  function wireServingsStepper(baseServings) {
    const decEl = document.querySelector('[data-action="servings-down"]');
    const incEl = document.querySelector('[data-action="servings-up"]');
    const valueEl = document.querySelector("#servings-value");
    if (!decEl || !incEl || !valueEl) return;

    let current = baseServings;
    decEl.addEventListener("click", () => {
      current = Math.max(1, current - 1);
      valueEl.textContent = current;
    });
    incEl.addEventListener("click", () => {
      current += 1;
      valueEl.textContent = current;
    });
  }

  function wireSaveButton(recipe) {
    const saveBtn = document.querySelector("#save-btn");
    if (!saveBtn) return;

    if (Auth.isSignedIn()) {
      saveBtn.textContent = "Save recipe";
    }

    saveBtn.addEventListener("click", () => {
      if (!Auth.isSignedIn()) {
        window.location.href = `login.html?next=${encodeURIComponent(`detail.html?id=${recipe.id}`)}`;
        return;
      }
      saveBtn.textContent = "Saved ✓";
      saveBtn.disabled = true;
    });
  }

  /** Shared handler for both login.html and register.html forms. */
  function initAuthForm() {
    const isRegister = document.body.dataset.page === "register";
    const form = document.querySelector("#auth-form");
    const alertEl = document.querySelector("#form-alert");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      alertEl.classList.remove("is-visible");
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalLabel = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = isRegister ? "Creating account…" : "Signing in…";

      try {
        const email = form.email.value.trim();
        const password = form.password.value;
        const user = isRegister
          ? await Api.register(form.name.value.trim(), email, password)
          : await Api.login(email, password);

        Auth.setUser(user);
        const params = new URLSearchParams(window.location.search);
        window.location.href = params.get("next") || "index.html";
      } catch (err) {
        alertEl.textContent = err.message;
        alertEl.classList.add("is-visible");
        submitBtn.disabled = false;
        submitBtn.textContent = originalLabel;
      }
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();

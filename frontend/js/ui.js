/**
 * ui.js
 * The only file that touches the DOM's event listeners and decides what
 * happens on each page. Each page sets <body data-page="..."> so this one
 * script can be included everywhere and just run the matching init.
 */
(() => {
  function markField(form, name) {
    let field = form.elements.namedItem(name);
    if (!field && name === "display_name") field = form.elements.namedItem("name");
    if (!field || !field.setAttribute) return;
    field.setAttribute("aria-invalid", "true");
  }

  function markErrorFields(form, error) {
    (error.fields || []).forEach((name) => markField(form, name));
  }

  function watchFieldEdits(form) {
    const clear = (event) => {
      const field = event.target;
      if (field?.removeAttribute) field.removeAttribute("aria-invalid");
    };
    form.addEventListener("input", clear);
    form.addEventListener("change", clear);
    form.addEventListener("invalid", (event) => {
      event.target?.setAttribute?.("aria-invalid", "true");
    }, true);
  }

  function init() {
    const page = document.body.dataset.page;
    const initializers = {
      home: initHome,
      list: initList,
      detail: initDetail,
      login: initAuthForm,
      register: initAuthForm,
      create_recipe: initCreateRecipe,
      userhome: initUserHome
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
      grid.innerHTML = `<div class="empty-state"><h3>Recipes didn't load</h3><p class="lede">${Render.errorAlert(err.message)}</p></div>`;
    }
  }

  async function initList() {
    const grid = document.querySelector("#recipe-grid");
    const chipsEl = document.querySelector("#category-chips");
    const searchInput = document.querySelector("#search-input");
    const ratingFilter = document.querySelector("#rating-filter");
    const authorFilter = document.querySelector("#author-filter");
    const advancedSearchButton = document.querySelector("#advanced-search-btn");
    const resultCount = document.querySelector("#result-count");
    const categories = window.APP_CONFIG.CATEGORIES;

    const params = new URLSearchParams(window.location.search);
    let activeCategory = params.get("category") || "all";
    let query = params.get("q") || "";
    let minRating = "";
    let author = "";
    if (searchInput) searchInput.value = query;

    chipsEl.innerHTML = Render.categoryChips(categories, activeCategory);

    async function load() {
      grid.innerHTML = Render.cardSkeletonGrid(6);
      try {
        const recipes = await Api.getRecipes({ category: activeCategory, query, minRating, author });
        grid.innerHTML = Render.recipeCardList(recipes);
        if (resultCount) {
          resultCount.textContent = `${recipes.length} recipe${recipes.length === 1 ? "" : "s"}`;
        }
      } catch (err) {
        grid.innerHTML = `<div class="empty-state"><h3>Recipes didn't load</h3><p class="lede">${Render.errorAlert(err.message)}</p></div>`;
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

    advancedSearchButton?.addEventListener("click", () => {
      minRating = ratingFilter.value;
      author = authorFilter.value.trim();
      load();
    });

    ratingFilter?.addEventListener("change", () => {
      minRating = ratingFilter.value;
      load();
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
      initReviews(id);
    } catch (err) {
      headerEl.innerHTML = `<h1 class="h1">This recipe didn't load</h1><p class="lede">${Render.errorAlert(err.message)} <a href="list.html">Browse recipes</a></p>`;
      document.querySelector("#detail-aside")?.remove();
    }
  }

  async function initReviews(recipeId) {
    const formContainer = document.querySelector("#review-form-container");
    const list = document.querySelector("#reviews-list");
    if (!formContainer || !list) return;

    if (Auth.isSignedIn()) {
      formContainer.innerHTML = `
        <form id="review-form" class="auth-shell" style="margin:var(--space-5) 0;">
          <div class="field">
            <label for="review-rating">Your rating</label>
            <select id="review-rating" name="rating" required>
              <option value="5">5 — Loved it</option><option value="4">4 — Very good</option>
              <option value="3">3 — Good</option><option value="2">2 — Needs work</option>
              <option value="1">1 — Didn't like it</option>
            </select>
          </div>
          <div class="field">
            <label for="review-comment">Your comment</label>
            <textarea id="review-comment" name="comment" rows="4" maxlength="2000" required placeholder="What did you think of this recipe?"></textarea>
          </div>
          <p id="review-message" class="lede" role="status"></p>
          <button class="btn btn--primary" type="submit">Post rating and comment</button>
        </form>`;
      const reviewForm = formContainer.querySelector("#review-form");
      watchFieldEdits(reviewForm);
      reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        const button = form.querySelector('button[type="submit"]');
        const message = form.querySelector("#review-message");
        button.disabled = true;
        message.textContent = "Posting…";
        try {
          await Api.saveRecipeReview(recipeId, {
            rating: Number(form.rating.value),
            comment: form.comment.value.trim()
          });
          message.textContent = "Your rating and comment were posted.";
          await loadReviews();
        } catch (error) {
          message.textContent = error.message;
          markErrorFields(form, error);
        } finally {
          button.disabled = false;
        }
      });
    } else {
      formContainer.innerHTML = `<p class="lede" style="margin:var(--space-5) 0;">Want to rate or comment? <a href="login.html?next=${encodeURIComponent(`detail.html?id=${recipeId}`)}">Sign in</a>.</p>`;
    }

    await loadReviews();

    async function loadReviews() {
      list.replaceChildren();
      try {
        const reviews = await Api.getRecipeReviews(recipeId);
        if (!reviews.length) {
          list.innerHTML = "<p class=\"lede\">No ratings or comments yet. Be the first to share what you think.</p>";
          return;
        }
        for (const review of reviews) {
          const article = document.createElement("article");
          article.className = "section__head";
          article.style.cssText = "border-top:1px solid var(--color-line);padding:var(--space-4) 0;";
          const heading = document.createElement("h3");
          heading.className = "h3";
          heading.textContent = `${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)} · ${review.reviewer_name}`;
          const comment = document.createElement("p");
          comment.className = "lede";
          comment.textContent = review.comment;
          article.append(heading, comment);
          list.append(article);
        }
      } catch (error) {
        list.innerHTML = `<p class="lede">${Render.errorAlert(error.message)}</p>`;
      }
    }
  }

  async function initCreateRecipe() {
    const form = document.querySelector("#recipe-form");
    const alertEl = document.querySelector("#form-alert");
    if (!form) return;
    watchFieldEdits(form);

    await Auth.restoreSession();
    if (!Auth.isSignedIn()) {
      window.location.replace(`login.html?next=${encodeURIComponent("create_recipe.html")}`);
      return;
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      alertEl.classList.remove("is-visible");
      const button = form.querySelector('button[type="submit"]');
      button.disabled = true;
      button.textContent = "Publishing…";
      const ingredients = form.ingredients.value.split("\n").map((line) => {
        const [qty, ...itemParts] = line.split("|");
        return { qty: qty.trim(), item: itemParts.join("|").trim() };
      }).filter((ingredient) => ingredient.qty && ingredient.item);
      const steps = form.steps.value.split("\n").map((text) => text.trim())
        .filter(Boolean).map((text, index) => ({ title: `Step ${index + 1}`, text }));
      const payload = {
        title: form.title.value.trim(),
        summary: form.summary.value.trim(),
        category: form.category.value,
        minutes: Number(form.minutes.value),
        servings: Number(form.servings.value),
        difficulty: form.difficulty.value,
        tags: form.tags.value.split(",").map((tag) => tag.trim()).filter(Boolean),
        notes: form.notes.value.trim(),
        ingredients,
        steps
      };

      try {
        const recipe = await Api.createRecipe(payload);
        window.location.href = `detail.html?id=${recipe.id}`;
      } catch (error) {
        alertEl.textContent = error.message;
        markErrorFields(form, error);
        alertEl.classList.add("is-visible");
        button.disabled = false;
        button.textContent = "Publish recipe";
      }
    });
  }

  async function initUserHome() {
    const profileForm = document.querySelector("#profile-form");
    const passwordForm = document.querySelector("#password-form");
    const savedGrid = document.querySelector("#saved-recipes");
    const sharedGrid = document.querySelector("#shared-recipes");
    const pageMessage = document.querySelector("#userhome-message");

    try {
      const user = await Api.getCurrentUser();
      Auth.setUser(user);
      profileForm.display_name.value = user.display_name;
    } catch (error) {
      if (error.status === 401) {
        window.location.replace(`login.html?next=${encodeURIComponent("userhome")}`);
        return;
      }
      pageMessage.textContent = error.message;
      return;
    }
    loadSavedRecipes().catch((error) => {
      savedGrid.textContent = error.message;
    });
    loadSharedRecipes().catch((error) => {
      sharedGrid.textContent = error.message;
    });
    watchFieldEdits(profileForm);
    watchFieldEdits(passwordForm);

    profileForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const status = profileForm.querySelector("[role=status]");
      const button = profileForm.querySelector('button[type="submit"]');
      button.disabled = true;
      status.textContent = "Saving…";
      try {
        const user = await Api.updateAccount({ display_name: profileForm.display_name.value.trim() });
        Auth.setUser(user);
        status.textContent = "Your name was updated.";
      } catch (error) {
        status.textContent = error.message;
        markErrorFields(profileForm, error);
      } finally {
        button.disabled = false;
      }
    });

    passwordForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const status = passwordForm.querySelector("[role=status]");
      const button = passwordForm.querySelector('button[type="submit"]');
      const newPassword = passwordForm.new_password.value;
      if (newPassword !== passwordForm.confirm_password.value) {
        status.textContent = "The new passwords don't match. Type them again.";
        markField(passwordForm, "new_password");
        markField(passwordForm, "confirm_password");
        return;
      }
      button.disabled = true;
      status.textContent = "Saving…";
      try {
        await Api.updateAccount({
          current_password: passwordForm.current_password.value,
          new_password: newPassword
        });
        passwordForm.reset();
        status.textContent = "Your password was changed.";
      } catch (error) {
        status.textContent = error.message;
        markErrorFields(passwordForm, error);
      } finally {
        button.disabled = false;
      }
    });

    async function loadSavedRecipes() {
      const recipes = await Api.getSavedRecipes();
      if (!recipes.length) {
        savedGrid.innerHTML = '<p class="lede">You have no saved recipes yet. <a href="list.html">Browse recipes</a> and save one you like.</p>';
        return;
      }
      savedGrid.innerHTML = Render.recipeCardList(recipes);
      const cards = savedGrid.querySelectorAll(".recipe-card");
      recipes.forEach((recipe, index) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "btn btn--ghost btn--sm";
        button.textContent = "Remove from saved";
        button.addEventListener("click", async () => {
          button.disabled = true;
          try {
            await Api.unsaveRecipe(recipe.id);
            await loadSavedRecipes();
          } catch (error) {
            button.textContent = error.message;
            button.disabled = false;
          }
        });
        cards[index]?.append(button);
      });
    }

    async function loadSharedRecipes() {
      const recipes = await Api.getMyRecipes();
      if (!recipes.length) {
        sharedGrid.innerHTML = '<p class="lede">You haven’t shared any recipes yet. <a href="create_recipe.html">Share your first recipe</a>.</p>';
        return;
      }
      sharedGrid.innerHTML = Render.recipeCardList(recipes);
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

    saveBtn.addEventListener("click", async () => {
      if (!Auth.isSignedIn()) {
        window.location.href = `login.html?next=${encodeURIComponent(`detail.html?id=${recipe.id}`)}`;
        return;
      }
      saveBtn.disabled = true;
      try {
        await Api.saveRecipe(recipe.id);
        saveBtn.textContent = "Saved ✓";
      } catch (err) {
        saveBtn.textContent = err.message;
        saveBtn.disabled = false;
      }
    });
  }

  /** Shared handler for both login.html and register.html forms. */
  function initAuthForm() {
    const isRegister = document.body.dataset.page === "register";
    const form = document.querySelector("#auth-form");
    const alertEl = document.querySelector("#form-alert");
    if (!form) return;
    watchFieldEdits(form);

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      alertEl.classList.remove("is-visible");
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalLabel = submitBtn.textContent;
      submitBtn.disabled = true;
      submitBtn.textContent = isRegister ? "Creating account…" : "Signing in…";

      try {
        const password = form.password.value;
        let user;
        if (isRegister) {
          user = await Api.register(
            form.name.value.trim(),
            form.username.value.trim(),
            form.email.value.trim(),
            password
          );
        } else {
          await Api.login(form.identifier.value.trim(), password);
          try {
            user = await Api.getCurrentUser();
          } catch {
            throw new Error("You signed in, but we couldn't keep you signed in. Open the app from its usual website address and try again.");
          }
        }

        Auth.setUser(user);
        const params = new URLSearchParams(window.location.search);
        window.location.href = params.get("next") || "index.html";
      } catch (err) {
        alertEl.textContent = err.message;
        markErrorFields(form, err);
        alertEl.classList.add("is-visible");
        submitBtn.disabled = false;
        submitBtn.textContent = originalLabel;
      }
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();

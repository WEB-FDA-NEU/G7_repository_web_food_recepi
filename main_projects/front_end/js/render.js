/**
 * render.js
 * Turns data (from Api) into markup. Nothing here talks to the network or
 * listens for events — that's ui.js's job. Keeping the split means each
 * card/section can be tested or reused without a live fetch.
 */
const Render = (() => {
  const PLATE_ICONS = {
    breakfast: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="8"/><path d="M9 9c1-1 5-1 6 0"/></svg>',
    mains: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M7 3v7a2 2 0 0 0 2 2v9M7 3v9M10 3v7M17 3c-1.5 0-3 1.5-3 4s0 5 0 5v9"/></svg>',
    salads: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 12a8 8 0 0 1 16 0Z"/><path d="M4 12h16M8 12V9M12 12V7M16 12V9"/></svg>',
    soups: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 11h16l-1 3a6 6 0 0 1-12 0Z"/><path d="M8 11V8M12 11V7M16 11V8"/></svg>',
    baking: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="10" width="14" height="9" rx="1"/><path d="M7 10c0-3 2-5 5-5s5 2 5 5"/></svg>',
    desserts: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 20h12M8 20V12a4 4 0 0 1 8 0v8M12 8V4"/></svg>'
  };

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function stars(rating) {
    const full = Math.round(rating);
    return "★".repeat(full) + "☆".repeat(5 - full);
  }

  function plate(category) {
    const icon = PLATE_ICONS[category] || PLATE_ICONS.mains;
    return `<div class="plate plate--cat-${category}">${icon}</div>`;
  }

  /** One recipe card, used on the home page and the browse/list page. */
  function recipeCard(recipe) {
    return `
      <article class="recipe-card">
        ${plate(recipe.category)}
        <div class="recipe-card__meta">
          <span>${recipe.minutes} min</span>
          <span>·</span>
          <span>${escapeHtml(recipe.difficulty)}</span>
          <span class="recipe-card__rating">${stars(recipe.rating)}</span>
        </div>
        <h3 class="recipe-card__title">
          <a href="detail.html?id=${recipe.id}">${escapeHtml(recipe.title)}</a>
        </h3>
        <p class="recipe-card__summary">${escapeHtml(recipe.summary)}</p>
        <span class="tag">${escapeHtml(recipe.author)}</span>
      </article>
    `;
  }

  function recipeCardList(recipes) {
    if (!recipes.length) {
      return `
        <div class="empty-state">
          <h3>No recipes match that search</h3>
          <p class="lede">Try a different keyword or clear the category filter.</p>
        </div>
      `;
    }
    return `<div class="recipe-grid">${recipes.map(recipeCard).join("")}</div>`;
  }

  function cardSkeletonGrid(count = 6) {
    const skeleton = `
      <div class="recipe-card">
        <div class="skeleton" style="aspect-ratio:4/3;border-radius:6px;"></div>
        <div class="skeleton" style="height:14px;width:60%;"></div>
        <div class="skeleton" style="height:20px;width:90%;"></div>
        <div class="skeleton" style="height:14px;width:100%;"></div>
      </div>
    `;
    return `<div class="recipe-grid">${skeleton.repeat(count)}</div>`;
  }

  function categoryChips(categories, activeId = "all") {
    const all = [{ id: "all", label: "All" }, ...categories];
    return all
      .map(
        (c) => `<button class="chip" type="button" data-category="${c.id}" aria-pressed="${c.id === activeId}">${escapeHtml(c.label)}</button>`
      )
      .join("");
  }

  /** Ingredient + step markup for the detail page. */
  function recipeDetail(recipe) {
    const ingredients = recipe.ingredients
      .map(
        (i) => `<li><span>${escapeHtml(i.item)}</span><span class="receipt__qty">${escapeHtml(i.qty)}</span></li>`
      )
      .join("");

    const steps = recipe.steps
      .map(
        (s) => `
          <li>
            <div>
              <h3>${escapeHtml(s.title)}</h3>
              <p class="lede">${escapeHtml(s.text)}</p>
            </div>
          </li>
        `
      )
      .join("");

    return {
      header: `
        <span class="hero__eyebrow">${escapeHtml(recipe.category)}</span>
        <h1 class="h1">${escapeHtml(recipe.title)}</h1>
        <p class="lede">${escapeHtml(recipe.summary)}</p>
        <div class="recipe-card__meta" style="margin-top:1rem;">
          <span>${recipe.minutes} min</span>
          <span>·</span>
          <span>${escapeHtml(recipe.difficulty)}</span>
          <span>·</span>
          <span>By ${escapeHtml(recipe.author)}</span>
          <span class="recipe-card__rating">${stars(recipe.rating)} (${recipe.ratingCount})</span>
        </div>
      `,
      ingredients,
      steps: `<ol class="steps">${steps}</ol>`,
      notes: recipe.notes ? `<p class="lede">${escapeHtml(recipe.notes)}</p>` : ""
    };
  }

  function errorAlert(message) {
    return escapeHtml(message);
  }

  return {
    recipeCard,
    recipeCardList,
    cardSkeletonGrid,
    categoryChips,
    recipeDetail,
    stars,
    errorAlert
  };
})();

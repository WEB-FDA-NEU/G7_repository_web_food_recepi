/**
 * api.js
 * Every network-shaped call the app makes lives here. Nothing else in the
 * codebase should call fetch() directly — that keeps the mock swap-out to
 * a real backend a one-file change.
 */
const Api = (() => {
  const { MOCK_BASE, LIST_FILE, ITEM_FILE_PREFIX, FAKE_LATENCY_MS } = window.APP_CONFIG;

  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function fetchJson(path) {
    const res = await fetch(path, { cache: "no-store" });
    if (!res.ok) {
      throw new ApiError(`Request to ${path} failed with ${res.status}`, res.status);
    }
    return res.json();
  }

  class ApiError extends Error {
    constructor(message, status) {
      super(message);
      this.status = status;
    }
  }

  /**
   * Get the recipe list, optionally filtered by category and/or a text query.
   * Filtering happens client-side since the "API" is a static file — a real
   * backend would take these as query params instead.
   */
  async function getRecipes({ category, query } = {}) {
    await wait(FAKE_LATENCY_MS);
    const all = await fetchJson(`${MOCK_BASE}${LIST_FILE}`);

    return all.filter((recipe) => {
      const matchesCategory = !category || category === "all" || recipe.category === category;
      const matchesQuery =
        !query ||
        recipe.title.toLowerCase().includes(query.toLowerCase()) ||
        recipe.tags.some((tag) => tag.toLowerCase().includes(query.toLowerCase()));
      return matchesCategory && matchesQuery;
    });
  }

  /**
   * Get one recipe's full detail (ingredients, steps). Only recipe #1 has a
   * hand-written detail file in this mock; anything else falls back to a
   * lightly synthesized detail built from the list entry, so the detail
   * page still has something reasonable to render.
   */
  async function getRecipeById(id) {
    await wait(FAKE_LATENCY_MS);
    try {
      return await fetchJson(`${MOCK_BASE}${ITEM_FILE_PREFIX}${id}.json`);
    } catch (err) {
      const all = await fetchJson(`${MOCK_BASE}${LIST_FILE}`);
      const match = all.find((r) => String(r.id) === String(id));
      if (!match) throw new ApiError(`No recipe with id ${id}`, 404);
      return {
        ...match,
        ingredients: [
          { qty: "—", item: "Full ingredient list not added yet for this recipe." }
        ],
        steps: [
          { title: "Coming soon", text: "This recipe's step-by-step hasn't been written up yet." }
        ]
      };
    }
  }

  /** Fake auth — resolves/rejects like a real endpoint would, no network. */
  async function login(email, password) {
    await wait(FAKE_LATENCY_MS);
    if (!email || !password) {
      throw new ApiError("Email and password are required.", 400);
    }
    if (password.length < 4) {
      throw new ApiError("That email and password don't match our records.", 401);
    }
    return { name: email.split("@")[0], email };
  }

  async function register(name, email, password) {
    await wait(FAKE_LATENCY_MS);
    if (!name || !email || !password) {
      throw new ApiError("All fields are required.", 400);
    }
    if (password.length < 6) {
      throw new ApiError("Password must be at least 6 characters.", 400);
    }
    return { name, email };
  }

  return { getRecipes, getRecipeById, login, register, ApiError };
})();

/** Browser requests to the FastAPI backend. */
const Api = (() => {
  const { API_BASE } = window.APP_CONFIG;

  class ApiError extends Error {
    constructor(message, status) {
      super(message);
      this.status = status;
    }
  }

  async function fetchJson(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (options.body) headers.set("Content-Type", "application/json");

    const response = await fetch(path, {
      ...options,
      headers,
      credentials: "include",
      cache: "no-store"
    });
    if (!response.ok) {
      let message = `Request failed with ${response.status}`;
      try {
        message = (await response.json()).detail || message;
      } catch {}
      throw new ApiError(message, response.status);
    }
    return response.status === 204 ? null : response.json();
  }

  function normalizeRecipe(recipe) {
    return {
      ...recipe,
      author: recipe.owner_name,
      ratingCount: recipe.rating_count
    };
  }

  async function getRecipes({ category, query } = {}) {
    const params = new URLSearchParams({ page_size: "50" });
    if (category && category !== "all") params.set("category", category);
    if (query) params.set("q", query);
    const page = await fetchJson(`${API_BASE}/recipes?${params}`);
    return page.items.map(normalizeRecipe);
  }

  async function getRecipeById(id) {
    return normalizeRecipe(await fetchJson(`${API_BASE}/recipes/${id}`));
  }

  async function login(email, password) {
    return fetchJson(`${API_BASE}/auth/login`, {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
  }

  async function register(name, email, password) {
    return fetchJson(`${API_BASE}/auth/register`, {
      method: "POST",
      body: JSON.stringify({ display_name: name, email, password })
    });
  }

  async function saveRecipe(id) {
    return fetchJson(`${API_BASE}/me/saved/${id}`, { method: "POST" });
  }

  async function logout() {
    return fetchJson(`${API_BASE}/auth/logout`, { method: "POST" });
  }

  return { getRecipes, getRecipeById, login, register, saveRecipe, logout };
})();

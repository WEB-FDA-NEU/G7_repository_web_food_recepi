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
        const detail = (await response.json()).detail;
        if (typeof detail === "string") {
          message = detail;
        } else if (Array.isArray(detail)) {
          message = detail
            .map((item) => item.msg || "Invalid value")
            .join("; ");
        }
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

  async function login(identifier, password) {
    return fetchJson(`${API_BASE}/auth/login`, {
      method: "POST",
      body: JSON.stringify({ identifier, password })
    });
  }

  async function register(name, username, email, password) {
    return fetchJson(`${API_BASE}/auth/register`, {
      method: "POST",
      body: JSON.stringify({ display_name: name, username, email, password })
    });
  }

  async function saveRecipe(id) {
    return fetchJson(`${API_BASE}/me/saved/${id}`, { method: "POST" });
  }

  async function logout() {
    return fetchJson(`${API_BASE}/auth/logout`, { method: "POST" });
  }

  async function getCurrentUser() {
    return fetchJson(`${API_BASE}/auth/me`);
  }

  async function getAdminUsers() {
    return fetchJson(`${API_BASE}/admin/users`);
  }

  async function getAdminStats() {
    return fetchJson(`${API_BASE}/admin/stats`);
  }

  return {
    getRecipes,
    getRecipeById,
    login,
    register,
    saveRecipe,
    logout,
    getCurrentUser,
    getAdminUsers,
    getAdminStats
  };
})();

// Shared with auth.js and the custom elements, which access the API through
// window.Api.
window.Api = Api;

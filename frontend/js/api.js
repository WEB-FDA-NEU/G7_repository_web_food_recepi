/** Browser requests to the FastAPI backend. */
const Api = (() => {
  const { API_BASE } = window.APP_CONFIG;

  class ApiError extends Error {
    constructor(message, status, fields = []) {
      super(message);
      this.status = status;
      this.fields = fields;
    }
  }

  async function fetchJson(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (options.body) headers.set("Content-Type", "application/json");

    let response;
    try {
      response = await fetch(path, {
        ...options,
        headers,
        credentials: "include",
        cache: "no-store"
      });
    } catch {
      throw new ApiError("We couldn't reach the app. Check your internet connection and try again.");
    }
    if (!response.ok) {
      let detail;
      try {
        detail = (await response.json()).detail;
      } catch {}
      throw new ApiError(
        userMessage(response.status, detail),
        response.status,
        invalidFields(response.status, detail)
      );
    }
    return response.status === 204 ? null : response.json();
  }

  function invalidFields(status, detail) {
    if (status === 401 && typeof detail === "string" && /incorrect|doesn't match/i.test(detail)) {
      return ["identifier", "password"];
    }
    if (status === 409 && typeof detail === "string") {
      return [/username/i.test(detail) ? "username" : "email"];
    }
    if (status === 400 && typeof detail === "string" && /current password/i.test(detail)) {
      return ["current_password"];
    }
    if (status === 422 && typeof detail === "string") {
      if (/current password/i.test(detail)) return ["current_password"];
      if (/name/i.test(detail)) return ["display_name"];
    }
    if (status !== 422 || !Array.isArray(detail)) return [];

    const fieldMap = {
      display_name: "display_name", title: "title", summary: "summary",
      category: "category", minutes: "minutes", servings: "servings",
      difficulty: "difficulty", tags: "tags", notes: "notes",
      ingredients: "ingredients", qty: "ingredients", item: "ingredients",
      steps: "steps", text: "steps", timer_minutes: "steps",
      identifier: "identifier", password: "password", username: "username",
      email: "email", rating: "rating", comment: "comment",
      current_password: "current_password", new_password: "new_password"
    };
    return [...new Set(detail.map((error) => {
      for (const part of [...(error.loc || [])].reverse()) {
        if (fieldMap[part]) return fieldMap[part];
      }
      return null;
    }).filter(Boolean))];
  }

  function userMessage(status, detail) {
    if (status === 401) {
      if (typeof detail === "string" && /incorrect|doesn't match/i.test(detail)) {
        return "That email or password doesn't match. Check them and try again.";
      }
      return "Please sign in again to continue.";
    }
    if (status === 403) return "You don't have permission to do that.";
    if (status === 404) return "We couldn't find that recipe. Browse recipes to find another one.";
    if (status === 400 && typeof detail === "string" && /current password/i.test(detail)) {
      return "That password is incorrect. Check it and try again.";
    }
    if (status === 400 && typeof detail === "string" && /new name or password/i.test(detail)) {
      return "Enter a new name or password.";
    }
    if (status === 400) return "We couldn't save that change. Check your information and try again.";
    if (status === 409) {
      if (typeof detail === "string" && /username/i.test(detail)) {
        return "That username is already in use. Choose another one.";
      }
      return "That email is already in use. Sign in or use another email.";
    }
    if (status === 422 && typeof detail === "string") {
      if (/current password/i.test(detail)) return "Enter your current password.";
      if (/your name/i.test(detail)) return "Enter your name.";
      return "Check the information and try again.";
    }
    if (status === 422 && Array.isArray(detail)) {
      const fieldNames = {
        title: "recipe title", summary: "description", category: "category",
        minutes: "cooking time", servings: "servings", difficulty: "difficulty",
        ingredients: "at least one ingredient", steps: "at least one step",
        identifier: "email or username", password: "password", display_name: "name",
        username: "username", email: "email", rating: "rating", comment: "comment",
        current_password: "current password", new_password: "new password"
      };
      const messages = detail.map((error) => {
        const field = fieldNames[error.loc?.at(-1)] || "this field";
        if (error.type === "missing") return `Enter ${field}.`;
        if (error.type === "string_too_short" || error.type === "too_short") {
          const minimum = error.ctx?.min_length;
          return minimum ? `Enter at least ${minimum} characters for the ${field}.` : `Add ${field}.`;
        }
        if (error.type === "greater_than" || error.type === "greater_than_equal") {
          return `Enter a valid ${field}.`;
        }
        if (error.type === "value_error" && error.loc?.at(-1) === "email") {
          return "Enter a valid email address.";
        }
        return `Check the ${field} and try again.`;
      });
      return [...new Set(messages)].join(" ");
    }
    return "We couldn't complete that. Please try again.";
  }

  function normalizeRecipe(recipe) {
    return {
      ...recipe,
      author: recipe.owner_name,
      ratingCount: recipe.rating_count
    };
  }

  async function getRecipes({ category, query, minRating, author } = {}) {
    const params = new URLSearchParams({ page_size: "50" });
    if (category && category !== "all") params.set("category", category);
    if (query) params.set("q", query);
    if (minRating) params.set("min_rating", minRating);
    if (author) params.set("author", author);
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

  async function createRecipe(recipe) {
    return fetchJson(`${API_BASE}/recipes`, {
      method: "POST",
      body: JSON.stringify(recipe)
    });
  }

  async function getRecipeReviews(id) {
    return fetchJson(`${API_BASE}/recipes/${id}/reviews`);
  }

  async function saveRecipeReview(id, review) {
    return fetchJson(`${API_BASE}/recipes/${id}/reviews`, {
      method: "POST",
      body: JSON.stringify(review)
    });
  }

  async function logout() {
    return fetchJson(`${API_BASE}/auth/logout`, { method: "POST" });
  }

  async function getCurrentUser() {
    return fetchJson(`${API_BASE}/auth/me`);
  }

  async function updateAccount(changes) {
    return fetchJson(`${API_BASE}/auth/me`, {
      method: "PATCH",
      body: JSON.stringify(changes)
    });
  }

  async function getSavedRecipes() {
    const recipes = await fetchJson(`${API_BASE}/me/saved`);
    return recipes.map(normalizeRecipe);
  }

  async function getMyRecipes() {
    const recipes = await fetchJson(`${API_BASE}/me/recipes`);
    return recipes.map(normalizeRecipe);
  }

  async function unsaveRecipe(id) {
    return fetchJson(`${API_BASE}/me/saved/${id}`, { method: "DELETE" });
  }

  async function getAdminUsers() {
    return fetchJson(`${API_BASE}/admin/users`);
  }

  async function getAdminStats() {
    return fetchJson(`${API_BASE}/admin/stats`);
  }

  async function getAdminRecipes() {
    const recipes = await fetchJson(`${API_BASE}/admin/recipes`);
    return recipes.map(normalizeRecipe);
  }

  async function deleteAdminRecipe(id) {
    return fetchJson(`${API_BASE}/admin/recipes/${id}`, { method: "DELETE" });
  }

  async function getAdminComments() {
    return fetchJson(`${API_BASE}/admin/comments`);
  }

  async function deleteAdminComment(id) {
    return fetchJson(`${API_BASE}/admin/comments/${id}`, { method: "DELETE" });
  }

  return {
    getRecipes,
    getRecipeById,
    login,
    register,
    createRecipe,
    getRecipeReviews,
    saveRecipeReview,
    saveRecipe,
    logout,
    getCurrentUser,
    updateAccount,
    getSavedRecipes,
    getMyRecipes,
    unsaveRecipe,
    getAdminUsers,
    getAdminStats,
    getAdminRecipes,
    deleteAdminRecipe,
    getAdminComments,
    deleteAdminComment
  };
})();

// Shared with auth.js and the custom elements, which access the API through
// window.Api.
window.Api = Api;

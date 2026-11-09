/**
 * auth.js
 * Keeps the public user details used by the header. The HttpOnly session
 * cookie is managed by the backend and is never exposed to JavaScript.
 */
const Auth = (() => {
  const { SESSION_KEY } = window.APP_CONFIG;
  // Keep the last known display state available immediately after navigation.
  // The backend session is still verified on every page load below.
  let currentUser = (() => {
    try {
      const cached = JSON.parse(localStorage.getItem(SESSION_KEY));
      return cached && typeof cached === "object" ? cached : null;
    } catch {
      localStorage.removeItem(SESSION_KEY);
      return null;
    }
  })();
  let sessionChecked = false;

  function getUser() {
    return currentUser;
  }

  function setUser(user) {
    user = { ...user, name: user.display_name };
    currentUser = user;
    sessionChecked = true;
    localStorage.setItem(SESSION_KEY, JSON.stringify(user));
    window.dispatchEvent(new CustomEvent("auth:change", { detail: user }));
  }

  async function signOut() {
    try {
      await Api.logout();
    } catch {
      // Clear the local display state even if the server is unavailable.
    } finally {
      clearUser();
    }
  }

  function clearUser() {
    currentUser = null;
    sessionChecked = true;
    localStorage.removeItem(SESSION_KEY);
    window.dispatchEvent(new CustomEvent("auth:change", { detail: null }));
  }

  function isSignedIn() {
    return Boolean(getUser());
  }

  async function restoreSession() {
    // localStorage is only a display cache. Always ask the backend so a valid
    // HttpOnly cookie can restore the header even if that cache was cleared.
    if (!window.Api?.getCurrentUser) return;
    try {
      setUser(await Api.getCurrentUser());
    } catch {
      clearUser();
    }
  }

  return { getUser, setUser, signOut, isSignedIn, restoreSession };
})();

// Expose the auth module to the header custom element and browser console.
window.Auth = Auth;

document.addEventListener("DOMContentLoaded", () => Auth.restoreSession());

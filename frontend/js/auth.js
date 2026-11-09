/**
 * auth.js
 * Keeps the public user details used by the header. The HttpOnly session
 * cookie is managed by the backend and is never exposed to JavaScript.
 */
const Auth = (() => {
  const { SESSION_KEY } = window.APP_CONFIG;

  function getUser() {
    try {
      const raw = localStorage.getItem(SESSION_KEY);
      const session = raw ? JSON.parse(raw) : null;
      return session?.user || session || null;
    } catch {
      return null;
    }
  }

  function setUser(user) {
    user = { ...user, name: user.display_name };
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
    localStorage.removeItem(SESSION_KEY);
    window.dispatchEvent(new CustomEvent("auth:change", { detail: null }));
  }

  function isSignedIn() {
    return Boolean(getUser());
  }

  return { getUser, setUser, signOut, isSignedIn };
})();

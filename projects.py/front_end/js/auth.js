/**
 * auth.js
 * Session state for the mock app. There's no real server session, so a
 * signed-in user is just a small object in localStorage — enough to gate
 * a few UI states (header greeting, "save recipe" button) realistically.
 */
const Auth = (() => {
  const { SESSION_KEY } = window.APP_CONFIG;

  function getUser() {
    try {
      const raw = localStorage.getItem(SESSION_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  function setUser(user) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(user));
    window.dispatchEvent(new CustomEvent("auth:change", { detail: user }));
  }

  function signOut() {
    localStorage.removeItem(SESSION_KEY);
    window.dispatchEvent(new CustomEvent("auth:change", { detail: null }));
  }

  function isSignedIn() {
    return Boolean(getUser());
  }

  return { getUser, setUser, signOut, isSignedIn };
})();

/**
 * config.js
 * Central settings for the API and UI.
 */
window.APP_CONFIG = {
  API_BASE: window.location.port === "5500"
    ? `${window.location.protocol}//${window.location.hostname}:8000/api`
    : "/api",

  SESSION_KEY: "ladle_session",

  CATEGORIES: [
    { id: "breakfast", label: "Breakfast" },
    { id: "mains", label: "Mains" },
    { id: "salads", label: "Salads" },
    { id: "soups", label: "Soups" },
    { id: "baking", label: "Baking" },
    { id: "desserts", label: "Desserts" }
  ]
};

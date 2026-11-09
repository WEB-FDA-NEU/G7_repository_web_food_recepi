/**
 * config.js
 * Central, environment-style settings. In a real backend this is where
 * the API base URL and any keys would live. For this mock build, it just
 * points at the local JSON files that stand in for API responses.
 */
window.APP_CONFIG = {
  // Where "API" responses come from. Swap this for a real endpoint later
  // without touching any other file.
  MOCK_BASE: "mock/",
  LIST_FILE: "items.json",
  ITEM_FILE_PREFIX: "item-",

  // Simulated network latency, so loading states are visible instead of
  // instant (delete or set to 0 once a real API is wired up).
  FAKE_LATENCY_MS: 250,

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

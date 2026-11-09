document.addEventListener("DOMContentLoaded", async () => {
  const message = document.querySelector("#admin-message");
  const consolePanel = document.querySelector("#admin-console");
  const userCount = document.querySelector("#user-count");
  const databaseSize = document.querySelector("#database-size");
  const userTable = document.querySelector("#admin-users");

  try {
    const currentUser = await Api.getCurrentUser();
    if (currentUser.role !== "admin") {
      window.location.replace("index.html");
      return;
    }

    Auth.setUser(currentUser);
    const [users, stats] = await Promise.all([
      Api.getAdminUsers(),
      Api.getAdminStats()
    ]);
    userCount.textContent = stats.user_count.toLocaleString();
    databaseSize.textContent = stats.database_size_bytes == null
      ? "Unavailable"
      : formatBytes(stats.database_size_bytes);

    for (const user of users) {
      const row = document.createElement("tr");
      const values = [
        user.display_name,
        user.username,
        user.email,
        user.role,
        new Date(user.created_at).toLocaleDateString()
      ];
      for (const value of values) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.append(cell);
      }
      userTable.append(row);
    }

    message.hidden = true;
    consolePanel.hidden = false;
  } catch (error) {
    if (error.status === 401) {
      window.location.replace("login.html?next=admin_console");
      return;
    }
    if (error.status === 403) {
      window.location.replace("index.html");
      return;
    }
    message.textContent = "Could not load the admin console. Please try again.";
  }
});

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB", "TB"];
  let value = bytes / 1024;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value.toFixed(1)} ${units[unit]}`;
}

document.addEventListener("DOMContentLoaded", async () => {
  const message = document.querySelector("#admin-message");
  const consolePanel = document.querySelector("#admin-console");
  const userCount = document.querySelector("#user-count");
  const userTable = document.querySelector("#admin-users");

  try {
    const currentUser = await Api.getCurrentUser();
    if (currentUser.role !== "admin") {
      window.location.replace("index.html");
      return;
    }

    Auth.setUser(currentUser);
    const users = await Api.getAdminUsers();
    userCount.textContent = `${users.length} account${users.length === 1 ? "" : "s"}`;

    for (const user of users) {
      const row = document.createElement("tr");
      const values = [
        user.display_name,
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
      window.location.replace("login.html?next=admin.html");
      return;
    }
    if (error.status === 403) {
      window.location.replace("index.html");
      return;
    }
    message.textContent = "Could not load the admin console. Please try again.";
  }
});

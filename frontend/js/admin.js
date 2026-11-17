document.addEventListener("DOMContentLoaded", async () => {
  const message = document.querySelector("#admin-message");
  const consolePanel = document.querySelector("#admin-console");
  const userCount = document.querySelector("#user-count");
  const databaseSize = document.querySelector("#database-size");
  const userTable = document.querySelector("#admin-users");
  const recipeTable = document.querySelector("#admin-recipes");
  const commentTable = document.querySelector("#admin-comments");
  const actionMessage = document.querySelector("#admin-action-message");

  try {
    const currentUser = await Api.getCurrentUser();
    if (currentUser.role !== "admin") {
      window.location.replace("index.html");
      return;
    }

    Auth.setUser(currentUser);
    message.hidden = true;
    consolePanel.hidden = false;
    actionMessage.textContent = "Loading admin data…";

    const [usersResult, statsResult, recipesResult, commentsResult] = await Promise.allSettled([
      Api.getAdminUsers(),
      Api.getAdminStats(),
      Api.getAdminRecipes(),
      Api.getAdminComments()
    ]);
    for (const result of [usersResult, statsResult, recipesResult]) {
      if (result.status === "rejected") throw result.reason;
    }
    const users = usersResult.value;
    const stats = statsResult.value;
    const recipes = recipesResult.value;
    const comments = commentsResult.status === "fulfilled" ? commentsResult.value : [];
    if (commentsResult.status === "rejected") {
      actionMessage.textContent = "Comments can't load yet. Run the database setup in database/note.py, then refresh this page.";
    }
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

    for (const recipe of recipes) {
      const row = document.createElement("tr");
      row.dataset.recipeId = recipe.id;
      appendTextCell(row, recipe.title);
      appendTextCell(row, recipe.author);
      const actions = document.createElement("td");
      actions.append(deleteButton("Delete recipe", async (button) => {
        const confirmed = window.confirm(
          `Delete “${recipe.title}”? Its comments and saved links will also be removed. This cannot be undone.`
        );
        if (!confirmed) return;
        await runDelete(button, async () => {
          await Api.deleteAdminRecipe(recipe.id);
          row.remove();
          commentTable.querySelectorAll(`[data-recipe-id="${recipe.id}"]`).forEach((commentRow) => commentRow.remove());
          actionMessage.textContent = "Recipe deleted.";
        });
      }));
      row.append(actions);
      recipeTable.append(row);
    }

    for (const comment of comments) {
      const row = document.createElement("tr");
      row.dataset.recipeId = comment.recipe_id;
      appendTextCell(row, comment.recipe_title);
      appendTextCell(row, comment.reviewer_name);
      appendTextCell(row, `${comment.rating} / 5`);
      appendTextCell(row, comment.comment);
      const actions = document.createElement("td");
      actions.append(deleteButton("Delete comment", async (button) => {
        const confirmed = window.confirm("Delete this comment and rating? This cannot be undone.");
        if (!confirmed) return;
        await runDelete(button, async () => {
          await Api.deleteAdminComment(comment.id);
          row.remove();
          actionMessage.textContent = "Comment deleted.";
        });
      }));
      row.append(actions);
      commentTable.append(row);
    }

    if (commentsResult.status === "fulfilled") actionMessage.textContent = "";
  } catch (error) {
    if (error.status === 401) {
      window.location.replace("login.html?next=admin_console");
      return;
    }
    if (error.status === 403) {
      window.location.replace("index.html");
      return;
    }
    if (consolePanel.hidden) {
      message.textContent = "The admin page didn't load. Refresh the page and try again.";
    } else {
      actionMessage.textContent = "Some admin data couldn't load. Refresh the page and try again.";
    }
  }
});

function appendTextCell(row, value) {
  const cell = document.createElement("td");
  cell.textContent = value ?? "";
  row.append(cell);
}

function deleteButton(label, onClick) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "btn btn--ghost btn--sm admin-delete";
  button.textContent = label;
  button.addEventListener("click", () => onClick(button).catch((error) => {
    document.querySelector("#admin-action-message").textContent = error.message;
  }));
  return button;
}

async function runDelete(button, action) {
  button.disabled = true;
  try {
    await action();
  } finally {
    button.disabled = false;
  }
}

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

import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##import
    """)
    return


@app.cell
def _():
    from pathlib import Path
    import sqlite3
    import marimo as mo

    return Path, mo, sqlite3


@app.cell
def _(Path, sqlite3):
    database_path = Path(__file__).resolve().parent / "data.sqlite3"
    connection = sqlite3.connect(database_path)
    return (connection,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##init database
    """)
    return


@app.cell
def _(mo):
    create_table = mo.ui.run_button(label="create_table")
    return (create_table,)


@app.cell(hide_code=True)
def _(connection, create_table, mo):
    mo.stop(not create_table.value, output=create_table)
    mo.output.append(create_table)
    connection.executescript(
        """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                display_name TEXT NOT NULL,
                phone TEXT NOT NULL DEFAULT '',
                role TEXT NOT NULL DEFAULT 'user'
                    CHECK (role IN ('user', 'admin')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS login_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                cookie_token_hash TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL,
                revoked_at TEXT
            );

            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(160) NOT NULL,
                summary TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                category VARCHAR(20) NOT NULL,
                minutes INTEGER NOT NULL DEFAULT 0,
                servings INTEGER NOT NULL DEFAULT 4,
                difficulty VARCHAR(20) NOT NULL DEFAULT 'Easy',
                tags VARCHAR(200) NOT NULL DEFAULT '',
                cover_url VARCHAR(255) NOT NULL DEFAULT '',
                rating FLOAT NOT NULL DEFAULT 0,
                rating_count INTEGER NOT NULL DEFAULT 0,
                status VARCHAR(20) NOT NULL DEFAULT 'published',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                owner_id INTEGER NOT NULL REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL REFERENCES recipes(id),
                position INTEGER NOT NULL DEFAULT 0,
                qty VARCHAR(40) NOT NULL,
                item VARCHAR(160) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL REFERENCES recipes(id),
                position INTEGER NOT NULL DEFAULT 0,
                title VARCHAR(80) NOT NULL,
                text TEXT NOT NULL,
                timer_minutes INTEGER
            );

            CREATE TABLE IF NOT EXISTS saved_recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                recipe_id INTEGER NOT NULL REFERENCES recipes(id),
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT uq_saved_recipe UNIQUE (user_id, recipe_id)
            );

            CREATE TABLE IF NOT EXISTS recipe_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT uq_recipe_review_user UNIQUE (user_id, recipe_id)
            );

            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes(title);
            CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes(category);
            CREATE INDEX IF NOT EXISTS idx_recipes_status ON recipes(status);
            CREATE INDEX IF NOT EXISTS idx_recipes_created_at ON recipes(created_at);
            CREATE INDEX IF NOT EXISTS idx_recipes_owner_id ON recipes(owner_id);
            CREATE INDEX IF NOT EXISTS idx_ingredients_recipe_id_item
                ON ingredients(recipe_id, item);
            CREATE INDEX IF NOT EXISTS idx_login_sessions_user_id
                ON login_sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_login_sessions_expires_at
                ON login_sessions(expires_at);
            CREATE INDEX IF NOT EXISTS idx_recipe_reviews_recipe_id
                ON recipe_reviews(recipe_id);
            """
    )
    user_columns = {
        row[1] for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "username" not in user_columns:
        import re

        connection.execute("ALTER TABLE users ADD COLUMN username TEXT COLLATE NOCASE")
        used_usernames = set()
        for user_id, email in connection.execute(
            "SELECT id, email FROM users ORDER BY id"
        ).fetchall():
            base = re.sub(r"[^a-zA-Z0-9_]+", "_", email.partition("@")[0]).strip("_")
            base = (base or "user")[:24]
            username = base
            suffix = 1
            while username.casefold() in used_usernames:
                tail = str(suffix)
                username = f"{base[:30 - len(tail)]}{tail}"
                suffix += 1
            used_usernames.add(username.casefold())
            connection.execute(
                "UPDATE users SET username = ? WHERE id = ?", (username, user_id)
            )
    connection.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username "
        "ON users(username COLLATE NOCASE)"
    )
    connection.commit()
    return


@app.cell
def _(mo):
    seed_database = mo.ui.run_button(label="seed_database")
    return (seed_database,)


@app.cell(hide_code=True)
def _(Path, connection, mo, seed_database):
    mo.stop(not seed_database.value, output=seed_database)
    mo.output.append(seed_database)
    seed_path = Path(__file__).resolve().parent / "seed.sql"
    connection.executescript(seed_path.read_text(encoding="utf-8"))
    connection.commit()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##danger zone
    Drop all app tables and their data.
    """)
    return


@app.cell
def _(mo):
    drop_tables = mo.ui.run_button(label="drop all tables")
    return (drop_tables,)


@app.cell(hide_code=True)
def _(connection, drop_tables, mo):
    mo.stop(not drop_tables.value, output=drop_tables)
    mo.output.append(drop_tables)
    connection.executescript(
        """
        PRAGMA foreign_keys = OFF;
        DROP TABLE IF EXISTS saved_recipes;
        DROP TABLE IF EXISTS recipe_reviews;
        DROP TABLE IF EXISTS steps;
        DROP TABLE IF EXISTS ingredients;
        DROP TABLE IF EXISTS recipes;
        DROP TABLE IF EXISTS login_sessions;
        DROP TABLE IF EXISTS users;
        PRAGMA foreign_keys = ON;
        """
    )
    connection.commit()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##inspect
    """)
    return


@app.cell
def _(connection, mo):
    _df = mo.sql(
        f"""
        PRAGMA table_info(users);
        """,
        engine=connection
    )
    return


@app.cell
def _(connection, mo, users):
    _df = mo.sql(
        f"""
        SELECT * from users
        """,
        engine=connection
    )
    return


@app.cell
def _(connection, login_sessions, mo):
    _df = mo.sql(
        f"""
        Select * from login_sessions
        """,
        engine=connection
    )
    return


@app.cell
def _(connection, mo, recipes):
    _df = mo.sql(
        f"""
        Select * from recipes
        """,
        engine=connection
    )
    return


@app.cell
def _(connection, mo, sqlite_master):
    _df = mo.sql(
        f"""
        SELECT *
        FROM sqlite_master
        WHERE type = 'table'
        --ORDER BY name;
        """,
        engine=connection
    )
    return


if __name__ == "__main__":
    app.run()

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
    mo.stop(create_table.value, output=create_table)
    mo.output.append(create_table)
    connection.executescript(
        """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
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

            CREATE INDEX IF NOT EXISTS idx_login_sessions_user_id
                ON login_sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_login_sessions_expires_at
                ON login_sessions(expires_at);
            """
    )
    connection.commit()
    return


@app.cell
def _(mo):
    seed_database = mo.ui.run_button(label="seed_database")
    return (seed_database,)


@app.cell(hide_code=True)
def _(Path, connection, mo, seed_database):
    mo.stop(seed_database.value, output=seed_database)
    mo.output.append(seed_database)
    seed_path = Path(__file__).resolve().parent / "seed.sql"
    connection.executescript(seed_path.read_text(encoding="utf-8"))
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
        engine=connection,
    )
    return


@app.cell
def _(connection, mo, users):
    _df = mo.sql(
        f"""
        SELECT * from users
        """,
        engine=connection,
    )
    return


@app.cell
def _(connection, mo, sqlite_master):
    _df = mo.sql(
        f"""
        SELECT *
        FROM sqlite_master
        --WHERE type = 'table'
        --ORDER BY name;
        """,
        engine=connection,
    )
    return


if __name__ == "__main__":
    app.run()

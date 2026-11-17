# Ladle — Final Project Report

**Web Design and Programming · Final Project Report**  
**Product:** Ladle — recipe sharing website  
**Group:** G7 (team number not specified in repository)  
**Repository:** [WEB-FDA-NEU/G7_repository_web_food_recepi](https://github.com/WEB-FDA-NEU/G7_repository_web_food_recepi)  
**Live URL:** Not confirmed; local run instructions are below.  
**Demo accounts:** `admin@example.com` / `password` (admin); `priya@example.com` / `password` (user). Seed SQL also provides `dan`, `marisol`, and `wen` accounts at `password`.  
**Submitted:** 2026-11-17 (workspace date; confirm actual submission date)

> This report is based on the repository contents and Git history available locally. Items not evidenced there are marked for team confirmation. No test suite or test output was present in the files inspected, so this report does not claim tests passed.

## 1. Project Overview

Ladle is a recipe sharing site for people who want to discover, search, and save cooking recipes. Visitors can browse published recipes, open recipe details, and search by title, category, rating, author, ingredients, or review text. Signed-in users can post recipes, rate and comment on recipes, save recipes, and manage their account; administrators can review and remove recipes and comments. The central flow is browse/search → recipe details → save or review, with a second flow for registering and posting a recipe.

Since the mock-data stage, the project has added a FastAPI backend, persistent SQLAlchemy database, cookie-based login sessions, recipe and review APIs, saved recipes, an admin console, and advanced search. FastAPI serves the frontend from the same origin when run as documented. The repository does not record which screens from Milestone 2 were dropped or merged; confirm that with the team.

## 2. Features

| # | Feature | Screens | API endpoints | Status | Owner (from contribution notes) |
|---|---|---|---|---|---|
| 1 | Browse, filter, search, and paginate published recipes | `index.html`, `list.html` | `GET /api/recipes` | Completed in code; runtime persistence not independently verified | minhquang |
| 2 | View recipe details, ingredients, and steps | `detail.html` | `GET /api/recipes/{recipe_id}` | Completed in code | bế Thành Đạt / minhquang (confirm) |
| 3 | Register, log in/out, and manage account | `register.html`, `login.html`, account UI | `POST /api/auth/register`, `/login`, `/logout`; `GET/PATCH /api/auth/me` | Completed in code | bế Thành Đạt (frontend); minhquang (backend; confirm) |
| 4 | Create and share a recipe | `create_recipe.html`, `userhome.html` | `POST /api/recipes`; `GET /api/me/recipes` | Partially completed: create/list routes exist; verify current UI and upload behavior | Phan Hải Đăng |
| 5 | Rate and comment on a recipe | `detail.html`, `userhome.html` | `GET/POST /api/recipes/{recipe_id}/reviews` | Completed in code | Phan Hải Đăng |
| 6 | Save and unsave recipes; view saved list | `detail.html`, user area | `GET /api/me/saved`; `POST/DELETE /api/me/saved/{recipe_id}` | Completed in code | Team; confirm owner |
| 7 | Admin dashboard and moderation | `admin_console.html` | `/api/admin/stats`, `/users`, `/recipes`, `/comments`, delete routes | Completed in code | Bùi Khang Long |

**Core flow:** Home/Browse → Search results → Recipe detail → Save or review.  
**Creator flow:** Register/Login → Create recipe → View own recipes.

## 3. Technology Stack

| Layer | Technology | Version evidence | Use |
|---|---|---|---|
| Frontend | HTML, CSS, JavaScript | No framework/version declared | Static pages and browser `fetch` calls |
| Backend | FastAPI, Uvicorn | `pyproject.toml` declares FastAPI `>=0.141.1`, Uvicorn `>=0.54.0`; `src/requirements.txt` pins FastAPI 0.115.6, Uvicorn 0.34.0 | JSON API and static frontend hosting |
| ORM / database | SQLAlchemy, SQLite by default | `pyproject.toml` declares SQLAlchemy `>=2.1.1`; requirements file pins 2.0.36 | Relational models and persistence; `DATABASE_URL` can select another SQLAlchemy database |
| Validation | Pydantic | `pyproject.toml` declares `pydantic[email]>=2.13.5`; requirements pins 2.10.4 | Request validation and response schemas |
| Passwords | bcrypt | `pyproject.toml` declares `bcrypt>=5.0.0`; requirements pins 4.2.1 | Password hashing and verification |
| Login | Opaque random session token in HttpOnly cookie | No separate package version | Session token hash stored in database; default expiry is 60 minutes |
| Other | marimo | `pyproject.toml` declares `>=0.25.2` | Database note/maintenance notebook |
| Testing | Not documented | No test dependency or test files found in inspected project file list | Add and run tests before reporting test results |

**Version note:** The project dependency declarations conflict with the legacy `src/requirements.txt` pins. The installed versions could not be established from repository metadata, so the table reports declared values rather than claiming a `pip freeze` result.

## 4. System Architecture

```text
Browser: frontend/*.html + frontend/js/*.js
  | fetch('/api/...', credentials included by browser for same-origin cookies)
  v
FastAPI: src/main.py
  |-- src/routers/auth.py       login, registration, profile
  |-- src/routers/recipes.py    recipe search, detail, reviews, saved recipes
  |-- src/routers/admin.py      admin statistics and moderation
  |-- src/deps.py               session and admin authorization
  v
SQLAlchemy models (src/models.py) → SQLite (database/data.sqlite3 by default)
```

FastAPI mounts the `frontend` directory at `/` after registering API routes, so the documented local app uses one origin and does not need CORS. CORS is configured for a separately served frontend on port 5500 during development. Uploaded files, if used, are served from `src/uploads`.

## 5. API Reference

Auth: **—** public; **L** signed-in user; **A** administrator. Request and response bodies are summarized; see `/docs` for generated schemas.

| Method | Path | Auth | Request | Success | Common errors | Owner |
|---|---|---:|---|---|---|---|
| GET | `/api/health` | — | — | `200 {status}` | — | — |
| POST | `/api/auth/register` | — | email, username, password, display name, optional phone | `201 UserOut` + session cookie | `409`, `422` | Backend; confirm |
| POST | `/api/auth/login` | — | identifier (email or username), password | `200 UserOut` + session cookie | `401`, `422` | Backend; confirm |
| POST | `/api/auth/logout` | — | session cookie if present | `204`; cookie cleared | — | Backend; confirm |
| GET | `/api/auth/me` | L | — | `200 UserOut` | `401` | Backend; confirm |
| PATCH | `/api/auth/me` | L | display name and/or current/new password | `200 UserOut` | `400`, `401`, `422` | Backend; confirm |
| GET | `/api/recipes` | — | category, `q`, `advanced_q`, `min_rating`, author, include/exclude categories, page, page_size | `200 RecipePage` | `422` | minhquang (search) |
| GET | `/api/recipes/{recipe_id}` | — | — | `200 RecipeDetail` | `404` | Backend; confirm |
| POST | `/api/recipes` | L | recipe fields, ingredients, steps | `201 RecipeDetail` | `401`, `422` | Phan Hải Đăng (feature; backend owner confirm) |
| GET | `/api/recipes/{recipe_id}/reviews` | — | — | `200 Review[]` | `404` | Phan Hải Đăng |
| POST | `/api/recipes/{recipe_id}/reviews` | L | rating 1–5, comment | `200 ReviewOut` (creates or updates the user's review) | `401`, `404`, `422` | Phan Hải Đăng |
| GET | `/api/me/recipes` | L | — | `200 RecipeCard[]` | `401` | Phan Hải Đăng |
| GET | `/api/me/saved` | L | — | `200 RecipeCard[]` | `401` | Confirm |
| POST | `/api/me/saved/{recipe_id}` | L | — | `201 {saved: true}`; repeat save is idempotent | `401`, `404` | Confirm |
| DELETE | `/api/me/saved/{recipe_id}` | L | — | `204` | `401` | Confirm |
| GET | `/api/admin/stats` | A | — | `200` counts and DB size | `401`, `403` | Bùi Khang Long |
| GET | `/api/admin/users` | A | — | `200 AdminUserOut[]` | `401`, `403` | Bùi Khang Long |
| GET | `/api/admin/recipes` | A | — | `200 RecipeCard[]` | `401`, `403` | Bùi Khang Long |
| DELETE | `/api/admin/recipes/{recipe_id}` | A | — | `204` | `401`, `403`, `404` | Bùi Khang Long |
| GET | `/api/admin/comments` | A | — | `200 ReviewOut[]` | `401`, `403` | Bùi Khang Long |
| DELETE | `/api/admin/comments/{review_id}` | A | — | `204` | `401`, `403`, `404` | Bùi Khang Long |

**Changes from mock/API contract:** Current backend uses `/api/recipes` and `/api/me` resources, typed recipe fields, and opaque cookie sessions. A prior mock contract was not present to compare field-by-field.

## 6. Database Design

```text
users 1 ───< recipes 1 ───< ingredients
   │             │  └────< steps
   │             ├───────< recipe_reviews >──── 1 users
   ├────< login_sessions
   └────< saved_recipes >────────────────────── 1 recipes
```

**Key constraints:** `users.email` and `users.username` are unique; `login_sessions.cookie_token_hash` is unique; `(saved_recipes.user_id, recipe_id)` and `(recipe_reviews.user_id, recipe_id)` are unique; child records reference their parent/user IDs with foreign keys. Recipe creation stores ordered ingredients and steps as separate rows. Recipe tags are stored as comma-separated text. Indexes cover recipe title/category/status/date/owner and common child lookups.

**Seed data:** `database/seed.sql` inserts five demo users (one admin, four standard users), nine sample recipes, and example ingredients/steps for a recipe. Demo password is `password`; stored values are bcrypt hashes. `database/note.py` contains database initialization and maintenance logic, consistent with the repository's agent instructions.

## 7. Authentication and Authorization

| Question | Implementation |
|---|---|
| Password storage | bcrypt hash in `users.password_hash`; this field is excluded from public user schemas. |
| Login result and storage | API returns public `UserOut`; server sets a random `login_session` HttpOnly cookie. Only a SHA-256 hash of the token is stored in `login_sessions`. |
| Validity | `SESSION_EXPIRE_MINUTES`, default 60 minutes; logout revokes the session and clears the cookie. |
| Login required | Recipe creation, review submission, current-user/profile routes, saved recipes, and all admin routes. |
| Role check | Admin routes require role `admin`; a non-admin receives `403`. Missing, expired, or revoked session receives `401`. |
| Frontend protection | Admin page checks `/api/auth/me` and redirects to login; API dependencies enforce access on the server regardless of the UI. |

**Unauthenticated request proof:** The backend dependency in `src/deps.py` raises HTTP 401 with `{"detail":"Please sign in to continue."}` when a protected route receives no session cookie. This is the response implied by code; no live curl request was run for this report.

## 8. Business Rules

| ID | Rule | Enforced in | Violation behavior | Test |
|---|---|---|---|---|
| BR-1 | Only a signed-in user may create a recipe, submit a review, or manage saved recipes. | `src/routers/recipes.py` via `get_current_user` | `401` | No test file/output found |
| BR-2 | A user can have at most one review per recipe; submitting again edits that review and refreshes the recipe's average/count. | `src/routers/recipes.py:save_review`; unique constraint in `src/models.py` | Existing review updated | No test file/output found |
| BR-3 | A user can save a recipe only once; repeated saves remain successful. | `src/routers/recipes.py:save_recipe`; unique constraint in `src/models.py` | Duplicate insert rolled back; returns `{saved: true}` | No test file/output found |
| BR-4 | Only admins can access moderation endpoints. | `src/deps.py:get_admin`; `src/routers/admin.py` | `401` if unauthenticated, `403` if non-admin | No test file/output found |
| BR-5 | Recipe input must include at least one ingredient and one step; title, summary, timing, servings, and review rating have validation limits. | `src/schemas.py` | `422` validation response | No test file/output found |

## 9. Testing

No test suite or actual `$ pytest -q` output was present in the repository files inspected. The template requires real command output, so the result is **not available** and should be filled after the team runs its tests. This report does not claim a pass count.

| Test | What it should prove | Owner |
|---|---|---|
| Not present in repository | Add coverage for login required, recipe creation validation, review uniqueness/average updates, saved-recipe idempotency, and admin role enforcement. | Team |

## 10. Team Members and Individual Contributions

The names/tasks below come from `CONTRIBUTION.md`; author counts come from `git shortlog -sne --all`. Commit counts are only a rough activity proxy and do not establish individual effort. Shares are normalized from the six author identities (same email aliases combined) and should be confirmed by the team. Student IDs and communication counts were not provided.

| No. | Student ID | Name | Frontend | Backend / files | Commits | Share* | Status |
|---:|---|---|---|---|---:|---:|---|
| 1 | Not provided | Bế Thành Đạt (`th3dummyking`; alias `dummyking`) | Frontend, site components | Frontend work noted; leader | 23 | 35% | Confirm with member |
| 2 | Not provided | Phan Hải Đăng (`phandang2310`) | User home | Recipe posting and reviews | 10 | 15% | Confirm with member |
| 3 | Not provided | minhquang (`mq`; alias `iambadwithname`) | Recipe search | Backend and search | 26 | 39% | Confirm with member |
| 4 | Not provided | Bùi Khang Long (`longbk761-bot`) | Admin console | Admin endpoints | 7 | 11% | Confirm with member |

\* Commit-based percentages rounded to total 100%; the 26 commits combine `mq` (21) and `iambadwithname` (5), while `th3dummyking` and `dummyking` share an email (20+3). Git shortlog output: `26 mq/iambadwithname; 23 th3dummyking/dummyking; 10 phandang2310; 7 longbk761-bot`.

## 11. How to Run

```sh
git clone https://github.com/WEB-FDA-NEU/G7_repository_web_food_recepi.git
cd G7_repository_web_food_recepi
uv sync
uv run uvicorn src.main:app --reload --port 10000
```

Open `http://127.0.0.1:10000` for the website and `http://127.0.0.1:10000/docs` for the API. The project defaults to SQLite at `database/data.sqlite3`.

| Environment variable | Meaning | Example/default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string | Defaults to local `database/data.sqlite3` |
| `SESSION_EXPIRE_MINUTES` | Login session lifetime | `60` |
| `COOKIE_SECURE` | Set Secure cookie flag for HTTPS | `true` in HTTPS deployment; default `false` |
| `CORS_ORIGINS` | Allowed separate frontend origins | Defaults to localhost and 127.0.0.1 on port 5500 |

**Known setup issue:** `pyproject.toml` and `src/requirements.txt` declare different dependency versions. Use the `uv` workflow from README unless the team has reconciled those manifests.

## 12. Known Issues and Future Work

| Issue / missing evidence | Why unresolved / evidence | Suggested next step |
|---|---|---|
| No automated test suite/output found | Not included among inspected repository files | Add tests for auth, recipe, review, saved, and admin behavior; report real `pytest -q` output |
| Dependency versions conflict | Current `pyproject.toml` ranges differ from legacy requirements pins | Choose one dependency source and lock compatible versions |
| Upload route not found | App serves `/uploads`, but no upload API endpoint was found in the routers | Confirm whether recipe cover images are local/static or implement and document upload handling |
| Team metadata incomplete | No student IDs, live deployment URL, communication counts, or confirmed workload shares | Fill from team records and verify each member's code ownership |
| Schema bootstrap/seed workflow unclear | `database/seed.sql` exists; README documents `uv sync` and server start but not an explicit seed command | Document the supported initialization/seed command and verify clean-database setup |

## 13. Use of AI Tools and External Sources

The template asks the team to disclose tools used by each member. This report was drafted with ChatGPT from the local repository and the supplied report template. This does not establish whether AI tools or external sources were used to build the application; each member should confirm their own disclosure.

| Tool / source | Used for | Files | Who |
|---|---|---|---|
| ChatGPT (report drafting) | Inspecting the supplied template and repository; drafting this report | `project-report.md`, report PDF | Report author; confirm attribution |
| External sources used for application | Not documented in repository | Not documented | Each member to confirm |

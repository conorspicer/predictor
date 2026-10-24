# NFL Predictor

A preserved NFL score-prediction game for four friends. This repository is offline;
there is no live service or production database to migrate. The compatibility branch
keeps the game runnable with synthetic data while repairing its security problems.
[PROJECT.md](PROJECT.md) records the original idea, scoring rules and unfinished parts.

## Run the fictional demo

Requires Python 3.11–3.14. The demo uses SQLite and includes the leaderboard; no
external account, historic database export or MySQL installation is needed.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-core.txt
export DJANGO_DEBUG=true DATABASE_ENGINE=sqlite
export SQLITE_DATABASE_PATH="$PWD/demo.sqlite3"
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in as `conorspicer` with
`demo-only-predictor`. All four example players use that fictional demo password;
only the first is an administrator. This is development data, not anyone's old
account or password. The demo has completed, closed and editable games plus
playoff choices, so the main screens have useful examples immediately.

`seed_demo` requires development mode and an empty database. It refuses to replace
existing data. Choose another unused `SQLITE_DATABASE_PATH` to create another demo.
The debug-only Django signing key is generated at startup; set a private
`DJANGO_SECRET_KEY` to keep local sessions across server restarts.

## Verify behavior

```sh
python manage.py test --settings=predictor.test_settings
python manage.py makemigrations --check --dry-run --settings=predictor.test_settings
```

The tests create a separate database. They cover the score calculation in both
Python and SQL, picks and their deadlines, ownership and scorekeeper permissions,
signup/login/logout, older password hashes, playoff forms, image validation, and
a fresh four-player demo including the admin and leaderboard pages.

GitHub Actions runs the suite on Python 3.11 and 3.14 with SQLite and Python 3.12
with MySQL 8.4. It also audits the installed dependencies. Dependabot checks Python
requirements and GitHub Actions weekly. Vendored jQuery provenance is recorded in
[static/VENDOR.md](static/VENDOR.md).

## What the compatibility branch changes

- Use supported, patched Django, Pillow, sqlparse and jQuery packages.
- Restrict match-score editing to `fixtures.change_fixture` or a superuser.
- Enforce the UI's stated one-hour-before-kickoff pick deadline on every save and
  use the same boundary for all public pick pages.
- Reject forged row IDs, fixture reassignment and invalid submissions; show errors.
- Replace the frozen 2024 week clock with the active schedule or an explicit
  `SEASON_WEEK_ONE_END` (ISO 8601 Wednesday 05:00 UTC after week one).
- Repair leaderboard view identifiers, POST logout, and missing-kickoff handling.
- Add a repeatable local demo and checks for the preserved behavior.

The original `master` history and its pre-fix commit `88e5808` remain intact. Public
secrets, database exports and bytecode are removed from this branch's files; earlier
commits still contain them. No old account data is restored for the demo.

## Optional MySQL setup

The original database backend remains supported with MySQL 8.0.11+ or MariaDB 10.5+.
Install `requirements.txt` instead of `requirements-core.txt`, configure
`DATABASE_ENGINE=mysql` and the `DATABASE_*` environment variables listed in
`.env.example`, then run `migrate`, `seed_demo` and `runserver` in development mode.
The native mysqlclient package requires MySQL client headers and pkg-config.

`python manage.py install_score_views` installs or replaces just `user_scores` and
`user_week_results`. SQLite adapts the original SQL syntax; the scoring definition
is shared. Use the demo or explicit provisioning for the historic weekly-result
backing rows. `.env` is not loaded automatically.

For MySQL test runs, use a disposable database and `PREDICTOR_TEST_MYSQL=1` with the
normal database environment settings. Django creates its separate test database.

Outside development mode the app requires `DJANGO_SECRET_KEY` and enables HTTPS
redirects and secure cookies. HSTS preload is opt-in. Hosting or deployment is not
part of this preservation work.

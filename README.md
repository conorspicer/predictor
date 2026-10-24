# NFL Predictor

Django app for weekly score predictions and a season leaderboard.

## Requirements

Python 3.11–3.14. Production leaderboards use MySQL 8.0.11+ (or MariaDB 10.5+).
The app uses Django 5.2 LTS; the older Django 4.1 release is unsupported.

## Local preview and tests

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-core.txt
python manage.py test --settings=predictor.test_settings
export DJANGO_DEBUG=true DATABASE_ENGINE=sqlite
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Tests always use a separate database. SQLite supports local login, fixtures and
picks; the leaderboard requires the MySQL views described below. Create synthetic
fixtures and picks in Django admin for a local preview. Do not restore the old
public database exports. To retain local sessions across server restarts, set a
private `DJANGO_SECRET_KEY`; the debug-only fallback is generated at startup.

## Production upgrade

1. Back up the live database privately and record the current deployment revision.
2. Confirm Python and database versions meet the requirements above before
   changing the existing virtual environment.
3. Set `DJANGO_SECRET_KEY` to a new, private random value in the host environment.
   The old key was committed publicly; do not reuse it or keep it as a fallback.
   Rotating it signs out existing sessions and invalidates old signed tokens.
4. Keep `DJANGO_DEBUG=false`. Set `DATABASE_USER`, `DATABASE_PASSWORD`,
   `DATABASE_HOST`, and optionally `DATABASE_NAME` and `DATABASE_PORT`.
   `.env.example` lists settings, but the app does not load `.env` automatically.
   Set them in the WSGI host environment without committing credentials.
5. In the new Python virtual environment, run:

   ```sh
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python manage.py check --deploy
   python manage.py migrate --plan
   python manage.py migrate
   python manage.py install_score_views
   python manage.py collectstatic --noinput
   ```

6. Configure the host's `/static/` mapping to `staticfiles/`, reload the WSGI app,
   and verify login/logout, an ordinary user's denied score-editor access, a pick
   save, a locked pick, and the leaderboard. If TLS terminates at a proxy, confirm
   its header behavior before enabling `DJANGO_TRUST_PROXY_HTTPS=true`; otherwise
   an incorrect proxy setup can cause HTTPS redirect loops.

The deployment check intentionally reports `security.W021`: browser HSTS preload
is not enabled automatically. HTTPS redirects, secure cookies and a one-hour HSTS
policy are enabled in production.

MySQL client headers and `pkg-config` are needed to build `mysqlclient`. On macOS,
the upstream driver documents `brew install mysql-client pkg-config` and setting
`PKG_CONFIG_PATH` to the installed mysql-client `lib/pkgconfig` directory. The
SQLite preview intentionally avoids that native dependency.

`install_score_views` replaces only the `user_scores` and `user_week_results`
views in the configured database; it does not replace stored fixtures or picks.
Keep a private copy of the previous view definitions for rollback. Existing
`results_userweekresult` rows and `UserTotalResult` entries still need season setup.

## Competition rules and permissions

- Only a user with `fixtures.change_fixture` (or a superuser) can edit match scores.
  Grant that permission to trusted scorekeepers through Django admin.
- A weekly pick closes exactly one hour before kickoff. All public pick routes
  use that same deadline; each player's own history stays visible to them.
- The `lock` checkbox retains its existing meaning; it does not change the
  server-enforced kickoff deadline or scoring rules.
- Week rollover remains Wednesday at 05:00 UTC. It is inferred from the earliest
  active week-one fixture, or can be set with the ISO 8601 `SEASON_WEEK_ONE_END`.
  Mark previous-season fixtures inactive (`changeable=false`) when loading a new
  schedule. No current-season schedule is fabricated by this upgrade.
- The leaderboard keeps its existing 30–20 home-team default for blank picks.
  Its four named player columns and manual season provisioning are existing
  limitations; new players need explicit setup.

## Exposed data and credentials

Database dumps and Python bytecode have been removed from the working branch and
are ignored going forward. Earlier Git commits and existing clones still contain
them. Review account password resets and invalidate old sessions before returning
the app to service. The September 2023 SendGrid notice says the exposed email key
was deleted; configure a fresh key only if email sending is reintroduced.
Any Git history cleanup requires coordination with people who hold old clones.

## Automated checks

GitHub Actions checks Python 3.11 and 3.14 against SQLite and runs the same tests,
real leaderboard-view tests, and a dependency audit against MySQL 8.4. Run MySQL
tests locally only against a disposable database using `PREDICTOR_TEST_MYSQL=1`
and the normal `DATABASE_*` settings. Django creates a separate test database.
Dependabot checks Python requirements and GitHub Actions weekly. Vendored jQuery
provenance is recorded in `static/VENDOR.md` and needs manual release review.

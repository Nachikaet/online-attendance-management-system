# Deployment Guide

## Before deployment
1. Push this folder to a private or public Git repository.
2. Set a long random `SECRET_KEY`.
3. Set `SEED_DEMO=false` and set unique demo credentials only if demonstration accounts are required.
4. Use a managed PostgreSQL database for a persistent hosted deployment. SQLite is intended for local use and single-instance demos.
5. Confirm the host's current free-tier rules, sleep behavior, database persistence, bandwidth limits and region availability. Free tiers change; do not assume permanent free service.
6. Do not use real student records until the school approves hosting, access controls, privacy, retention and backup arrangements.

## Generic Python host steps
1. Create a Python web service connected to the repository.
2. Build/install command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`
4. Configure environment variables:
   - `SECRET_KEY`: long random secret
   - `DATABASE_URL`: managed PostgreSQL connection string
   - `SEED_DEMO=false` for non-demo deployment
5. Deploy and open the provider-generated HTTPS URL.
6. Create/verify administrator access. If demo seeding was disabled before first run, create an admin through a controlled one-time setup process before opening the site publicly; do not expose a public registration endpoint.
7. Test login, attendance save, report filtering, CSV export, role restrictions, and backup/restore.

## Free hosting considerations
Provider free plans and product names change. Choose a provider that supports Python WSGI apps and a persistent PostgreSQL database. A free web service may sleep when idle, and a free database may have size/retention limits. If no suitable persistent free database is available, use SQLite only for a temporary demo, not for a multi-user school deployment.

## Local backup
On a local SQLite deployment, sign in as administrator and open `/backup` to download the database. Test restoration by copying the backup to a separate test directory and launching the app against that copy.

## Migration
Set `DATABASE_URL` to the destination database, install dependencies, configure `SECRET_KEY`, and deploy with `gunicorn app:app`. For database engine changes, export/import records and verify constraints and date handling. See `docs/PORTABILITY.md`.

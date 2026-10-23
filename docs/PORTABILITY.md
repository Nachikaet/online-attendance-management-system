# Portability Testing and Migration Report
## Portability approach
- Client interface uses HTML, CSS, Bootstrap and browser JavaScript.
- Server uses Python and Flask, supported on Windows, Linux and macOS for development and Linux-based WSGI hosting for deployment.
- SQLAlchemy abstracts database access; SQLite is default for local evaluation and PostgreSQL is recommended for hosted multi-user use.
- Runtime configuration is read from environment variables rather than hard-coded host-specific paths.
- `requirements.txt` declares dependencies; `Procfile` documents a WSGI start command.
## Target matrix
| Target | Method | Status |
|---|---|---|
| Windows 10/11 | Python virtual environment + browser | To be tested |
| Linux | Python virtual environment + browser | To be tested |
| Android | Chrome browser against hosted URL | To be tested |
| iOS/iPadOS | Safari browser against hosted URL | To be tested |
| Chrome | Run core workflow | To be tested |
| Edge | Run core workflow | To be tested |
| Firefox | Run core workflow | To be tested |
| Safari | Run core workflow | To be tested |
## Migration procedure
1. Back up current database and verify the backup.
2. Install a supported Python version on destination environment.
3. Copy repository and install `requirements.txt`.
4. Set a new strong `SECRET_KEY` and destination `DATABASE_URL`.
5. Provision PostgreSQL for a persistent hosted deployment; migrate records with an export/import or migration utility.
6. Set `SEED_DEMO=false` for non-demo use.
7. Deploy using `gunicorn app:app`.
8. Test login, role restrictions, attendance uniqueness, reports, CSV export and backup/restore.
9. Compare student/attendance record counts before and after migration.
## Limitations
The cross-browser and device matrix is a test plan, not proof of completed tests. The application has not been independently security audited. Database migration between SQLite and PostgreSQL should be verified with representative data. Free hosting policies and persistence guarantees depend on the selected provider.

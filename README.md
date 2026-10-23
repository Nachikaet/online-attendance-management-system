# Online Attendance Management System
**For:** Sankar Matriculation School, Sankagiri West, Namakkal District, Tamil Nadu

## Features implemented
- Separate administrator and teacher login roles
- Password hashing and session-based authentication
- Administrator student management (add, edit, archive, search and filter)
- Administrator teacher-account creation and subject list management
- Attendance marking by date, class and section (Present / Absent / Leave)
- Daily dashboard counts
- Date-range attendance reports and automatically calculated percentages
- CSV report export
- SQLite database backup download for local deployments
- Responsive Bootstrap interface
- SQLAlchemy models and environment-based configuration for portability

## Run locally (Windows, macOS, Linux)
Install Python 3.11+ (Python 3.12 recommended).
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Demo accounts (local demo only)
- Administrator: `admin` / `ChangeMe123!`
- Teacher: `teacher1` / `Teacher123!`

Change these passwords before any public deployment. Do not put real student information into a public demo.

## Project documents
- `docs/SRS.md` — software requirements specification
- `docs/TEST_PLAN.md` — test cases and results template
- `docs/PORTABILITY.md` — portability and migration report
- `docs/USER_MANUAL.md` — user manual
- `DEPLOYMENT.md` — hosting and deployment guide
- `schema.sql` — relational schema reference

## Important notes
This is a functional academic starter implementation, not a security-audited production system. Before real school use, configure a strong secret, disable demo seeding, replace demo credentials, enable HTTPS, add CSRF protection and rate limiting, test backups/restores, and obtain school approval for student-data handling. Attendance percentage here is Present / records marked in the selected date range; school policy may instead require eligible school days as the denominator. This application does not yet implement class-subject timetable periods or an audit log.

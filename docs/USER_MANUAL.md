# User Manual
## Sign in
Open the application URL and enter your assigned username and password. Use Logout when finished.
## Administrator
- Students: add records with unique admission number, name, class and section; search/filter; edit; archive.
- Teachers: create teacher accounts. Use a unique username and password of at least eight characters.
- Subjects: add subject names to the subject list.
- Backup: on local SQLite installations, select the database backup link from the dashboard.
## Teacher and administrator
- Attendance: choose date, class and section; select Present, Absent or Leave for each student; save attendance.
- Reports: choose start/end dates and optional class/section/name filter; review totals and percentage; export CSV.
## Attendance percentage
The current calculation is Present records divided by all attendance records marked for that student in the selected date range. Unmarked school days are not included. Confirm this rule with school policy before operational use.
## Demo credentials
Local demo only: admin / ChangeMe123! and teacher1 / Teacher123!. Change these before public deployment. Never use demo credentials for real school data.
## Troubleshooting
- App will not start: check Python version and run `pip install -r requirements.txt`.
- Login fails: check username/password and confirm the account is active.
- Hosted data disappears: verify that a persistent database is configured; local ephemeral files may be lost on redeploy.
- Access denied: teacher accounts cannot access administrator-only student, teacher and subject management.

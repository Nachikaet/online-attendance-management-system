# Software Requirements Specification (SRS)
## 1. Introduction
### 1.1 Purpose
Specify a browser-based attendance management system for Sankar Matriculation School, Sankagiri West, Namakkal District, Tamil Nadu.
### 1.2 Scope
The system provides role-based access for administrators and teachers, student records, attendance marking, reports, percentages, filtering, CSV export and backup support.
### 1.3 Definitions
- Administrator: manages student and teacher records and subjects.
- Teacher: marks attendance and views reports.
- Attendance percentage: present records divided by attendance records marked in the selected range, multiplied by 100.
## 2. Overall description
### 2.1 User classes
Administrator and teacher.
### 2.2 Operating environment
A Python Flask web application accessible via a modern web browser. Supported target operating systems are Windows, Linux, Android and iOS through the browser.
### 2.3 Constraints
Requires network access for hosted use. Persistent production hosting requires a persistent database and configured secrets. Free hosting plans may sleep or impose storage/usage limits.
## 3. Functional requirements
- FR-01: The system shall authenticate administrators and teachers.
- FR-02: The system shall restrict administrator-only functions to the administrator role.
- FR-03: Administrators shall add, edit, search, filter and archive student records.
- FR-04: Administrators shall create teacher accounts.
- FR-05: Administrators shall maintain a subject list.
- FR-06: Authorized users shall mark students Present, Absent or Leave by date, class and section.
- FR-07: The system shall prevent duplicate attendance records for one student on one date.
- FR-08: Authorized users shall filter reports by date range, class, section and student name/admission number.
- FR-09: The system shall calculate attendance percentages automatically.
- FR-10: Authorized users shall export report data as CSV.
- FR-11: Administrators shall download a local SQLite database backup.
- FR-12: The system shall show dashboard attendance counts for the current date.
## 4. Non-functional requirements
- NFR-01 Portability: use a browser-based UI and Python/Flask backend; no client-side installation required.
- NFR-02 Compatibility: test current Chrome, Edge, Firefox and Safari.
- NFR-03 Responsiveness: Bootstrap layout adapts to desktop, tablet and phone widths.
- NFR-04 Performance: routine school-sized queries should complete promptly; verify using realistic data.
- NFR-05 Reliability: database constraints prevent duplicate daily records; backups must be tested.
- NFR-06 Maintainability: separate templates, application logic, models and documentation.
- NFR-07 Security: password hashes, authenticated sessions, role checks, input validation and environment-based secrets.
- NFR-08 Cost: use open-source components and a free-tier host when available; document restrictions.
## 5. Data requirements
Student: admission number, name, class, section, active flag. User: username, password hash, role and active flag. Attendance: student, date, status and marking user. Subject: name.
## 6. Acceptance criteria
All test cases in `TEST_PLAN.md` should pass; deployed URL should be tested from a second device; the source should install from a clean environment; backup restoration and role restrictions should be demonstrated.
## 7. Known limitations / future work
Add CSRF protection, rate limiting, password reset, audit logs, teacher-to-class assignment, timetable periods, attendance correction approvals, bulk CSV student import, PDF reports, automated backup scheduling and a formal admin bootstrap command before production use.

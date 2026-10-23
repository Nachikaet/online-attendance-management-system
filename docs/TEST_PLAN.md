# Test Plan and Test Results
Run tests on a clean local installation and record the actual result/date/device. Do not claim a test passed until executed.

| ID | Test | Steps | Expected result | Result |
|---|---|---|---|---|
| TC-01 | Admin login | Sign in as admin with valid credentials | Dashboard opens | Pending execution |
| TC-02 | Invalid login | Enter incorrect password | Error message; no login | Pending execution |
| TC-03 | Teacher login | Sign in as teacher | Dashboard opens | Pending execution |
| TC-04 | Role restriction | Teacher opens `/students` directly | HTTP 403 | Pending execution |
| TC-05 | Add student | Admin adds unique admission number | Student appears in list | Pending execution |
| TC-06 | Duplicate admission | Add an existing admission number | Validation message | Pending execution |
| TC-07 | Edit student | Change name/class/section | Updated details persist | Pending execution |
| TC-08 | Archive student | Archive a student | Hidden from active lists; history retained | Pending execution |
| TC-09 | Mark attendance | Mark class/section for a date | Statuses persist | Pending execution |
| TC-10 | Update attendance | Change status for same student/date | Existing row updates; no duplicate | Pending execution |
| TC-11 | Report date filter | Select date range | Only records in range are counted | Pending execution |
| TC-12 | Attendance percentage | Create known present/absent rows | Present / marked records × 100 | Pending execution |
| TC-13 | CSV export | Export selected date range | Valid CSV downloads | Pending execution |
| TC-14 | Backup | Admin opens `/backup` on SQLite | Database file downloads | Pending execution |
| TC-15 | Mobile layout | Open pages on phone-sized viewport | No horizontal overflow in main forms | Pending execution |
| TC-16 | Unknown route | Open nonexistent path | Friendly 404 page | Pending execution |
| TC-17 | Unauthenticated route | Open `/reports` while logged out | Redirect to login | Pending execution |
| TC-18 | Browser compatibility | Repeat core workflow in Chrome/Edge/Firefox/Safari | Core workflow works | Pending execution |
| TC-19 | Migration | Restore/export data to test deployment | Record counts and totals match | Pending execution |
| TC-20 | Backup restore | Restore a backup in isolated test environment | Application reads restored data | Pending execution |

## Test execution record
- Tester:
- Date:
- OS/device:
- Browser/version:
- App version/commit:
- Actual failures and screenshots:
- Retest notes:

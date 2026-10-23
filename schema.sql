-- Reference schema. The application creates equivalent tables via SQLAlchemy.
CREATE TABLE app_user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('admin','teacher')),
  teacher_name VARCHAR(120),
  active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE student (
  id INTEGER PRIMARY KEY,
  admission_no VARCHAR(40) UNIQUE NOT NULL,
  name VARCHAR(120) NOT NULL,
  class_name VARCHAR(40) NOT NULL,
  section VARCHAR(20) NOT NULL DEFAULT 'A',
  active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE attendance (
  id INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES student(id),
  attendance_date DATE NOT NULL,
  status VARCHAR(12) NOT NULL CHECK (status IN ('Present','Absent','Leave')),
  marked_by INTEGER NOT NULL REFERENCES app_user(id),
  UNIQUE(student_id, attendance_date)
);
CREATE TABLE subject (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL
);

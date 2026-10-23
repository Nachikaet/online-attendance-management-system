import os
import csv
import io
from datetime import date, datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-this-secret")
database_url = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "attendance.db"))
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    teacher_name = db.Column(db.String(120), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_no = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(40), nullable=False)
    section = db.Column(db.String(20), nullable=False, default="A")
    active = db.Column(db.Boolean, default=True, nullable=False)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(12), nullable=False)
    marked_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    student = db.relationship("Student", backref="attendance_records")
    marker = db.relationship("User")
    __table_args__ = (
        db.UniqueConstraint("student_id", "attendance_date", name="unique_student_date"),
    )


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapped


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                return redirect(url_for("login"))
            if session.get("role") not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapped
    return decorator


@app.context_processor
def inject_globals():
    return {
        "current_user": session.get("username"),
        "current_role": session.get("role")
    }


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username, active=True).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            flash("Signed in successfully.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    today = date.today()
    students_count = Student.query.filter_by(active=True).count()
    today_records = Attendance.query.filter_by(attendance_date=today).all()

    present_count = sum(1 for r in today_records if r.status == "Present")
    absent_count = sum(1 for r in today_records if r.status == "Absent")
    leave_count = sum(1 for r in today_records if r.status == "Leave")

    return render_template(
        "dashboard.html",
        students_count=students_count,
        present_count=present_count,
        absent_count=absent_count,
        leave_count=leave_count,
        today=today
    )


@app.route("/students", methods=["GET", "POST"])
@roles_required("admin")
def students():
    if request.method == "POST":
        admission_no = request.form.get("admission_no", "").strip()
        name = request.form.get("name", "").strip()
        class_name = request.form.get("class_name", "").strip()
        section = request.form.get("section", "").strip().upper()

        if not all([admission_no, name, class_name, section]):
            flash("All student fields are required.", "danger")
        elif Student.query.filter_by(admission_no=admission_no).first():
            flash("Admission number already exists.", "danger")
        else:
            db.session.add(
                Student(
                    admission_no=admission_no,
                    name=name,
                    class_name=class_name,
                    section=section
                )
            )
            db.session.commit()
            flash("Student added.", "success")

        return redirect(url_for("students"))

    q = request.args.get("q", "").strip()
    class_filter = request.args.get("class_name", "").strip()
    section_filter = request.args.get("section", "").strip()

    query = Student.query.filter_by(active=True)

    if q:
        query = query.filter(
            db.or_(
                Student.name.ilike(f"%{q}%"),
                Student.admission_no.ilike(f"%{q}%")
            )
        )

    if class_filter:
        query = query.filter_by(class_name=class_filter)

    if section_filter:
        query = query.filter_by(section=section_filter)

    return render_template(
        "students.html",
        students=query.order_by(
            Student.class_name,
            Student.section,
            Student.name
        ).all(),
        q=q,
        class_filter=class_filter,
        section_filter=section_filter,
        classes=[
            x[0]
            for x in db.session.query(Student.class_name).distinct().all()
        ]
    )


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@roles_required("admin")
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == "POST":
        student.admission_no = request.form.get("admission_no", "").strip()
        student.name = request.form.get("name", "").strip()
        student.class_name = request.form.get("class_name", "").strip()
        student.section = request.form.get("section", "").strip().upper()

        if not all([
            student.admission_no,
            student.name,
            student.class_name,
            student.section
        ]):
            flash("All fields are required.", "danger")
        else:
            db.session.commit()
            flash("Student updated.", "success")
            return redirect(url_for("students"))

    return render_template("edit_student.html", student=student)


@app.route("/students/<int:student_id>/deactivate", methods=["POST"])
@roles_required("admin")
def deactivate_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.active = False
    db.session.commit()
    flash("Student archived. Historical attendance is retained.", "success")
    return redirect(url_for("students"))


@app.route("/teachers", methods=["GET", "POST"])
@roles_required("admin")
def teachers():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        teacher_name = request.form.get("teacher_name", "").strip()

        if not username or len(password) < 8 or not teacher_name:
            flash(
                "Name and username are required; password must be at least 8 characters.",
                "danger"
            )
        elif User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
        else:
            user = User(
                username=username,
                role="teacher",
                teacher_name=teacher_name
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Teacher account created.", "success")

        return redirect(url_for("teachers"))

    return render_template(
        "teachers.html",
        teachers=User.query.filter_by(role="teacher").order_by(User.username).all()
    )


@app.route("/subjects", methods=["GET", "POST"])
@roles_required("admin")
def subjects():
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name and not Subject.query.filter_by(name=name).first():
            db.session.add(Subject(name=name))
            db.session.commit()
            flash("Subject added.", "success")
        else:
            flash("Enter a new subject name.", "danger")

        return redirect(url_for("subjects"))

    return render_template(
        "subjects.html",
        subjects=Subject.query.order_by(Subject.name).all()
    )


@app.route("/attendance", methods=["GET", "POST"])
@roles_required("admin", "teacher")
def attendance():
    selected_date = request.values.get(
        "attendance_date",
        date.today().isoformat()
    )

    try:
        selected_day = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        selected_day = date.today()
        selected_date = selected_day.isoformat()

    class_name = request.values.get("class_name", "").strip()
    section = request.values.get("section", "").strip().upper()

    if request.method == "POST":
        class_name = request.form.get("class_name", "").strip()
        section = request.form.get("section", "").strip().upper()
        selected_date = request.form.get(
            "attendance_date",
            date.today().isoformat()
        )

        try:
            selected_day = datetime.strptime(
                selected_date, "%Y-%m-%d"
            ).date()
        except ValueError:
            flash("Invalid date.", "danger")
            return redirect(url_for("attendance"))

        # FIX: Empty class/section filters mean "all classes/sections".
        students_query = Student.query.filter_by(active=True)

        if class_name:
            students_query = students_query.filter_by(
                class_name=class_name
            )

        if section:
            students_query = students_query.filter_by(
                section=section
            )

        students_list = students_query.all()

        for student in students_list:
            status = request.form.get(
                f"status_{student.id}",
                "Absent"
            )

            if status not in ("Present", "Absent", "Leave"):
                continue

            record = Attendance.query.filter_by(
                student_id=student.id,
                attendance_date=selected_day
            ).first()

            if record:
                record.status = status
                record.marked_by = session["user_id"]
            else:
                db.session.add(
                    Attendance(
                        student_id=student.id,
                        attendance_date=selected_day,
                        status=status,
                        marked_by=session["user_id"]
                    )
                )

        db.session.commit()
        flash("Attendance saved.", "success")

        return redirect(
            url_for(
                "attendance",
                attendance_date=selected_date,
                class_name=class_name,
                section=section
            )
        )

    # Apply filters only when the user selects them.
    query = Student.query.filter_by(active=True)

    if class_name:
        query = query.filter_by(class_name=class_name)

    if section:
        query = query.filter_by(section=section)

    student_rows = query.order_by(
        Student.class_name,
        Student.section,
        Student.name
    ).all()

    records = {
        r.student_id: r.status
        for r in Attendance.query.filter_by(
            attendance_date=selected_day
        ).all()
    }

    classes = [
        x[0]
        for x in db.session.query(Student.class_name)
        .filter_by(active=True)
        .distinct()
        .all()
    ]

    sections = [
        x[0]
        for x in db.session.query(Student.section)
        .filter_by(active=True)
        .distinct()
        .all()
    ]

    return render_template(
        "attendance.html",
        students=student_rows,
        records=records,
        selected_date=selected_date,
        class_filter=class_name,
        section_filter=section,
        classes=classes,
        sections=sections
    )


@app.route("/reports")
@roles_required("admin", "teacher")
def reports():
    start = request.args.get(
        "start",
        (date.today() - timedelta(days=6)).isoformat()
    )
    end = request.args.get("end", date.today().isoformat())
    class_name = request.args.get("class_name", "").strip()
    section = request.args.get("section", "").strip().upper()
    q = request.args.get("q", "").strip()

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        start_date = date.today() - timedelta(days=6)
        end_date = date.today()
        start = start_date.isoformat()
        end = end_date.isoformat()

    student_query = Student.query.filter_by(active=True)

    if class_name:
        student_query = student_query.filter_by(class_name=class_name)

    if section:
        student_query = student_query.filter_by(section=section)

    if q:
        student_query = student_query.filter(
            db.or_(
                Student.name.ilike(f"%{q}%"),
                Student.admission_no.ilike(f"%{q}%")
            )
        )

    student_rows = student_query.order_by(
        Student.class_name,
        Student.section,
        Student.name
    ).all()

    report_rows = []

    for student in student_rows:
        recs = Attendance.query.filter(
            Attendance.student_id == student.id,
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        ).all()

        marked = len(recs)
        present = sum(1 for r in recs if r.status == "Present")
        absent = sum(1 for r in recs if r.status == "Absent")
        leave = sum(1 for r in recs if r.status == "Leave")
        percentage = (present / marked * 100) if marked else 0

        report_rows.append({
            "student": student,
            "marked": marked,
            "present": present,
            "absent": absent,
            "leave": leave,
            "percentage": percentage
        })

    classes = [
        x[0]
        for x in db.session.query(Student.class_name).distinct().all()
    ]

    return render_template(
        "reports.html",
        rows=report_rows,
        start=start,
        end=end,
        class_filter=class_name,
        section_filter=section,
        q=q,
        classes=classes
    )


@app.route("/reports/export")
@roles_required("admin", "teacher")
def export_report():
    start = request.args.get(
        "start",
        (date.today() - timedelta(days=6)).isoformat()
    )
    end = request.args.get("end", date.today().isoformat())

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        abort(400)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Admission No",
        "Student",
        "Class",
        "Section",
        "Days Marked",
        "Present",
        "Absent",
        "Leave",
        "Attendance %"
    ])

    students_list = Student.query.filter_by(active=True).order_by(
        Student.class_name,
        Student.section,
        Student.name
    ).all()

    for student in students_list:
        recs = Attendance.query.filter(
            Attendance.student_id == student.id,
            Attendance.attendance_date >= start_date,
            Attendance.attendance_date <= end_date
        ).all()

        if not recs:
            continue

        present = sum(r.status == "Present" for r in recs)
        absent = sum(r.status == "Absent" for r in recs)
        leave = sum(r.status == "Leave" for r in recs)

        writer.writerow([
            student.admission_no,
            student.name,
            student.class_name,
            student.section,
            len(recs),
            present,
            absent,
            leave,
            f"{present / len(recs) * 100:.2f}"
        ])

    data = io.BytesIO(output.getvalue().encode("utf-8-sig"))
    data.seek(0)

    return send_file(
        data,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"attendance_{start}_to_{end}.csv"
    )


@app.route("/backup")
@roles_required("admin")
def backup():
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
        path = app.config["SQLALCHEMY_DATABASE_URI"].replace(
            "sqlite:///",
            "",
            1
        )

        if os.path.exists(path):
            return send_file(
                path,
                as_attachment=True,
                download_name="attendance-backup.db"
            )

    flash(
        "For hosted databases, use your provider's database export/backup facility. See DEPLOYMENT.md.",
        "warning"
    )
    return redirect(url_for("dashboard"))


@app.errorhandler(403)
def forbidden(error):
    return render_template(
        "error.html",
        code=403,
        message="You do not have permission to access this page."
    ), 403


@app.errorhandler(404)
def not_found(error):
    return render_template(
        "error.html",
        code=404,
        message="The requested page was not found."
    ), 404


def seed_demo():
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="admin")
        admin.set_password(
            os.environ.get("DEMO_ADMIN_PASSWORD", "ChangeMe123!")
        )
        db.session.add(admin)

    if not User.query.filter_by(username="teacher1").first():
        teacher = User(
            username="teacher1",
            role="teacher",
            teacher_name="Demo Teacher"
        )
        teacher.set_password(
            os.environ.get("DEMO_TEACHER_PASSWORD", "Teacher123!")
        )
        db.session.add(teacher)

    if Student.query.count() == 0:
        db.session.add_all([
            Student(
                admission_no="SM001",
                name="Demo Student One",
                class_name="10",
                section="A"
            ),
            Student(
                admission_no="SM002",
                name="Demo Student Two",
                class_name="10",
                section="A"
            ),
            Student(
                admission_no="SM003",
                name="Demo Student Three",
                class_name="9",
                section="B"
            )
        ])

    if Subject.query.count() == 0:
        db.session.add_all([
            Subject(name="English"),
            Subject(name="Mathematics"),
            Subject(name="Science")
        ])

    db.session.commit()


with app.app_context():
    db.create_all()

    if os.environ.get("SEED_DEMO", "true").lower() == "true":
        seed_demo()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

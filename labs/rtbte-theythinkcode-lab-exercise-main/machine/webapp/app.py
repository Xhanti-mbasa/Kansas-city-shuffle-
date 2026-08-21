from __future__ import annotations

import os
import sqlite3
import random
import smtplib
from pathlib import Path
from email.message import EmailMessage

try:
    from flask import Flask, abort, redirect, render_template, request, send_from_directory, session, url_for
except ModuleNotFoundError as exc:  # pragma: no cover - clearer local error
    raise SystemExit(
        "Flask is not installed in this Python environment. Start the app with Docker "
        "using machine/webapp/start.sh, or install the requirements from "
        "machine/webapp/requirements.txt."
    ) from exc


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = Path(os.environ.get("APP_INSTANCE_DIR", "/tmp/soc-workshop-instance"))
DB_PATH = INSTANCE_DIR / "school.db"
UPLOAD_DIR = INSTANCE_DIR / "uploads"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "training-secret-key")
MAILHOG_HOST = os.environ.get("MAILHOG_HOST", "mailhog")
MAILHOG_PORT = int(os.environ.get("MAILHOG_PORT", "1025"))
MAIL_FROM = os.environ.get("MAIL_FROM", "no-reply@school.local")

BLUE_TEAM = [
    {
        "first_name": "Anele",
        "last_name": "Mthembu",
        "email": "anele.mthembu@thinkcode.local",
        "role": "Tier 1 Analyst",
        "phone": "+27 60 555 0101",
        "station": "SOC Pod 1",
    },
    {
        "first_name": "Mosa",
        "last_name": "Radebe",
        "email": "mosa.radebe@thinkcode.local",
        "role": "Tier 2 Analyst",
        "phone": "+27 60 555 0102",
        "station": "SOC Pod 2",
    },
    {
        "first_name": "Lerato",
        "last_name": "Sithole",
        "email": "lerato.sithole@thinkcode.local",
        "role": "Tier 3 Analyst",
        "phone": "+27 60 555 0103",
        "station": "SOC Pod 3",
    },
    {
        "first_name": "Kgosi",
        "last_name": "Mahlangu",
        "email": "kgosi.mahlangu@thinkcode.local",
        "role": "Incident Responder",
        "phone": "+27 60 555 0104",
        "station": "Response Desk",
    },
    {
        "first_name": "Nokuthula",
        "last_name": "Dlamini",
        "email": "nokuthula.dlamini@thinkcode.local",
        "role": "Threat Hunter",
        "phone": "+27 60 555 0105",
        "station": "Hunt Desk",
    },
    {
        "first_name": "Sibusiso",
        "last_name": "Ndlovu",
        "email": "sibusiso.ndlovu@thinkcode.local",
        "role": "Security Engineer",
        "phone": "+27 60 555 0106",
        "station": "Tooling Desk",
    },
    {
        "first_name": "Tebogo",
        "last_name": "Molefe",
        "email": "tebogo.molefe@thinkcode.local",
        "role": "Threat Intel Analyst",
        "phone": "+27 60 555 0107",
        "station": "Intel Desk",
    },
]


def db_conn() -> sqlite3.Connection:
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    conn = db_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            office TEXT NOT NULL,
            extension TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, password, role) VALUES (1, 'admin', 'admin123', 'admin')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO users (id, username, password, role) VALUES (2, 'support', 'support123', 'staff')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO notes (id, title, body) VALUES (1, 'Welcome', 'This is the school portal.')"
    )
    cur.execute(
        "INSERT OR IGNORE INTO notes (id, title, body) VALUES (2, 'Exam Schedule', 'Check the dashboard for the latest alerts.')"
    )
    seed_demo_accounts(cur)
    conn.commit()
    conn.close()
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def seed_demo_accounts(cur: sqlite3.Cursor) -> None:
    staff_profiles = [
        ("Nandi Mokoena", "nandi.mokoena@school.local", "Academic Affairs", "Block B-14", "2041"),
        ("Pieter Botha", "pieter.botha@school.local", "IT Services", "Block C-02", "2088"),
        ("Amina Hassan", "amina.hassan@school.local", "Student Support", "Block A-09", "2017"),
    ]
    student_profiles = [
        ("Lebo Nkosi", "lebo.nkosi@student.school.local", "Engineering", "Dorm 2", "3104"),
        ("Thando Dlamini", "thando.dlamini@student.school.local", "Business", "Dorm 5", "3158"),
        ("Mia Naidoo", "mia.naidoo@student.school.local", "Design", "Dorm 1", "3012"),
        ("Kagiso Molefe", "kagiso.molefe@student.school.local", "Science", "Dorm 3", "3220"),
        ("Zinhle Khumalo", "zinhle.khumalo@student.school.local", "Arts", "Dorm 4", "3299"),
    ]

    staff_accounts = [
        ("staff.nandi", "staff123", "staff", staff_profiles[0]),
        ("staff.pieter", "staff123", "staff", staff_profiles[1]),
        ("staff.amina", "staff123", "staff", staff_profiles[2]),
    ]
    student_accounts = [
        ("student.lebo", "student123", "student", student_profiles[0]),
        ("student.thando", "student123", "student", student_profiles[1]),
        ("student.mia", "student123", "student", student_profiles[2]),
        ("student.kagiso", "student123", "student", student_profiles[3]),
        ("student.zinhle", "student123", "student", student_profiles[4]),
    ]

    next_id = cur.execute("SELECT COALESCE(MAX(id), 2) + 1 AS next_id FROM users").fetchone()["next_id"]
    rng = random.Random(20260818)

    for username, password, role, profile in staff_accounts + student_accounts:
        cur.execute(
            "INSERT OR IGNORE INTO users (id, username, password, role) VALUES (?, ?, ?, ?)",
            (next_id, username, password, role),
        )
        if cur.rowcount:
            full_name, email, department, office, extension = profile
            # Add a little variety to the staff/student seed data while keeping it repeatable.
            if role == "staff":
                office = f"{office} / Suite {rng.randint(1, 7)}"
                extension = f"{rng.randint(2000, 2099)}"
            else:
                office = f"{office} / Room {rng.randint(1, 12)}"
                extension = f"{rng.randint(3000, 3999)}"
            cur.execute(
                """
                INSERT OR IGNORE INTO user_profiles
                (user_id, full_name, email, department, office, extension)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (next_id, full_name, email, department, office, extension),
            )
        next_id += 1


def create_user(username: str, password: str, role: str) -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password are required."
    if role not in {"student", "staff", "admin"}:
        return False, "Invalid role."
    conn = db_conn()
    try:
        cur = conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role),
        )
        user_id = cur.lastrowid
        full_name = username.replace(".", " ").title()
        email = f"{username}@school.local" if role == "staff" else f"{username}@student.school.local"
        department = "Staff Services" if role == "staff" else "Student Body"
        office = "Front Office" if role == "staff" else "Main Campus"
        extension = str(random.randint(2000, 2999) if role == "staff" else random.randint(3000, 3999))
        conn.execute(
            """
            INSERT INTO user_profiles
            (user_id, full_name, email, department, office, extension)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, full_name, email, department, office, extension),
        )
        conn.commit()
        send_welcome_email(email, full_name, role, username, password)
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    finally:
        conn.close()
    return True, "Account created."


def send_welcome_email(to_email: str, full_name: str, role: str, username: str, password: str) -> None:
    message = EmailMessage()
    message["Subject"] = f"Welcome to the School Portal, {full_name}"
    message["From"] = MAIL_FROM
    message["To"] = to_email
    message.set_content(
        "\n".join(
            [
                f"Hello {full_name},",
                "",
                f"Your {role} account has been created for the school portal.",
                f"Username: {username}",
                f"Password: {password}",
                "",
                "This message was captured by MailHog for the workshop.",
            ]
        )
    )
    try:
        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT, timeout=5) as smtp:
            smtp.send_message(message)
    except OSError:
        # Keep the lab usable even if MailHog is temporarily unavailable.
        pass


@app.before_request
def _startup() -> None:
    init_db()


@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/blue-team")
def blue_team():
    return render_template("blue_team.html", team=BLUE_TEAM)


@app.route("/student-signup", methods=["GET", "POST"])
def student_signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        ok, message = create_user(
            username,
            password,
            "student",
        )
        if ok:
            return render_template(
                "signup_success.html",
                account_type="Student",
                username=username,
                sound_url="https://www.myinstants.com/instant/aol-youve-got-mail/embed/",
            )
        return render_template("student_signup.html", error=message), 400
    return render_template("student_signup.html")


@app.route("/staff-signup", methods=["GET", "POST"])
def staff_signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        ok, message = create_user(
            username,
            password,
            "staff",
        )
        if ok:
            return render_template(
                "signup_success.html",
                account_type="Staff",
                username=username,
                sound_url="https://www.myinstants.com/instant/aol-youve-got-mail/embed/",
            )
        return render_template("staff_signup.html", error=message), 400
    return render_template("staff_signup.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    conn = db_conn()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()
    if not user:
        return render_template("login.html", error="Invalid credentials"), 401
    session["user"] = user["username"]
    session["role"] = user["role"]
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("index"))
    conn = db_conn()
    notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (session.get("user"),)).fetchone()
    profile = None
    if user:
        profile = conn.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user["id"],)).fetchone()
    staff_profiles = []
    if session.get("role") == "staff":
        staff_profiles = conn.execute(
            """
            SELECT u.username, p.full_name, p.email, p.department, p.office, p.extension
            FROM users u
            JOIN user_profiles p ON p.user_id = u.id
            WHERE u.role = 'staff'
            ORDER BY u.id
            """
        ).fetchall()
    conn.close()
    return render_template(
        "dashboard.html",
        notes=notes,
        user=session.get("user"),
        role=session.get("role"),
        profile=profile,
        staff_profiles=staff_profiles,
    )


@app.route("/admin")
def admin():
    if not session.get("user"):
        return redirect(url_for("index"))
    if session.get("role") != "admin":
        return render_template("admin.html", denied=True), 403
    conn = db_conn()
    users = conn.execute("SELECT id, username, role FROM users ORDER BY id").fetchall()
    profiles = conn.execute(
        """
        SELECT u.username, p.full_name, p.email, p.department, p.office, p.extension
        FROM users u
        JOIN user_profiles p ON p.user_id = u.id
        ORDER BY u.id
        """
    ).fetchall()
    conn.close()
    return render_template("admin.html", users=users, profiles=profiles, denied=False)


@app.route("/search")
def search():
    if not session.get("user"):
        return redirect(url_for("index"))
    q = request.args.get("q", "")
    conn = db_conn()
    query = f"SELECT * FROM notes WHERE title LIKE '%{q}%' OR body LIKE '%{q}%'"
    results = conn.execute(query).fetchall()
    conn.close()
    return render_template("search.html", query=q, results=results)


@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("user"):
        return redirect(url_for("index"))
    file = request.files.get("file")
    if not file:
        return redirect(url_for("dashboard"))
    dest = UPLOAD_DIR / file.filename
    file.save(dest)
    return redirect(url_for("dashboard"))


@app.route("/uploads/<path:filename>")
def uploads(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/files/")
@app.route("/files/<path:subpath>")
def files(subpath: str = ""):
    target = BASE_DIR / "public" / subpath
    if target.is_dir():
        return {"entries": sorted([p.name for p in target.iterdir()])}
    if target.exists():
        return send_from_directory(target.parent, target.name)
    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

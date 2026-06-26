from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
DATABASE = "attendance.db"

# ---------------------------
# Database Connection Helpers
# ---------------------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        reg_no = request.form["register_number"]
        name = request.form["name"]
        dept = request.form["department"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO students (reg_no, name, department) VALUES (?, ?, ?)",
                       (reg_no, name, dept))
        db.commit()
        return redirect(url_for("index"))
    return render_template("add_student.html")

@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():
    if request.method == "POST":
        reg_no = request.form["register_number"]
        date = request.form["date"]
        status = request.form["status"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO attendance (reg_no, date, status) VALUES (?, ?, ?)",
                       (reg_no, date, status))
        db.commit()
        return redirect(url_for("report"))
    return render_template("mark_attendance.html")

@app.route("/report")
def report():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT a.date, s.reg_no, s.name, s.department, a.status FROM attendance a JOIN students s ON a.reg_no = s.reg_no")
    records = cursor.fetchall()
    return render_template("report.html", records=records)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

# ---------------------------
# Database Initialization
# ---------------------------
def init_db():
    if not os.path.exists(DATABASE):
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reg_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                department TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reg_no TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (reg_no) REFERENCES students (reg_no)
            )
        """)
        db.commit()
        db.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

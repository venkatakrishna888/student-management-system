from flask import Blueprint, render_template, request, redirect, session
import mysql.connector

main = Blueprint('main', __name__)

# MySQL Connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="YOUR_PASSWORD",
    database="student_db"
)

cursor = db.cursor()


# ======================
# LOGIN
# ======================
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# ======================
# LOGOUT
# ======================
@main.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ======================
# HOME
# ======================
@main.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("index.html", students=students)

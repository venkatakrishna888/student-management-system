from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secretkey123"   # 🔐 required for login session

# MySQL Connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Krishna@506",   # 🔴 Change this
    database="student_db"
)

cursor = db.cursor()

# =========================
# LOGIN PAGE
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Simple admin login (you can change this)
        if username == "krishna" and password == "1234":
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# =========================
# HOME + SEARCH (Protected)
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        search = request.form["search"]

        sql = """SELECT * FROM students 
                 WHERE name LIKE %s 
                 OR email LIKE %s 
                 OR course LIKE %s 
                 OR phone LIKE %s"""
        
        values = ("%" + search + "%",) * 4
        cursor.execute(sql, values)
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    return render_template("index.html", students=students)

# =========================
# ADD STUDENT (Protected)
# =========================
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        phone = request.form["phone"]

        sql = "INSERT INTO students (name, email, course, phone) VALUES (%s, %s, %s, %s)"
        values = (name, email, course, phone)
        cursor.execute(sql, values)
        db.commit()

        return redirect("/")

    return render_template("add.html")

# =========================
# EDIT STUDENT (Protected)
# =========================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]
        phone = request.form["phone"]

        sql = "UPDATE students SET name=%s, email=%s, course=%s, phone=%s WHERE id=%s"
        values = (name, email, course, phone, id)
        cursor.execute(sql, values)
        db.commit()

        return redirect("/")

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    return render_template("edit.html", student=student)

# =========================
# DELETE STUDENT (Protected)
# =========================
@app.route("/delete/<int:id>")
def delete_student(id):
    if "user" not in session:
        return redirect("/login")

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return redirect("/")

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)

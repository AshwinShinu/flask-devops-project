from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import init_db, db, Student
import os

app = Flask(__name__)
DATABASE = os.getenv("DATABASE_URL", "sqlite:///database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app)

@app.route("/")
def index():
    students = Student.query.all()
    return render_template("index.html", students=students)

# API endpoints
@app.route("/api/students", methods=["GET"])
def list_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    s = Student.query.get_or_404(student_id)
    return jsonify(s.to_dict())

@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.json or request.form
    name = data.get("name")
    roll = data.get("roll")
    marks = data.get("marks", 0)
    s = Student(name=name, roll=roll, marks=marks)
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    s = Student.query.get_or_404(student_id)
    data = request.json or request.form
    s.name = data.get("name", s.name)
    s.roll = data.get("roll", s.roll)
    s.marks = data.get("marks", s.marks)
    db.session.commit()
    return jsonify(s.to_dict())

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    s = Student.query.get_or_404(student_id)
    db.session.delete(s)
    db.session.commit()
    return "", 204

# simple form-based add
@app.route("/add", methods=["POST"])
def add_form():
    name = request.form.get("name")
    roll = request.form.get("roll")
    marks = request.form.get("marks", 0)
    s = Student(name=name, roll=roll, marks=marks)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

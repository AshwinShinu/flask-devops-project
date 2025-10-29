from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend JS to call API

# Mock in-memory database
students = [
    {"id": 1, "name": "Alice", "roll": "101", "marks": 90},
    {"id": 2, "name": "Bob", "roll": "102", "marks": 85}
]

@app.route('/')
def index():
    return render_template('index.html')

# ✅ GET all students
@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students)

# ✅ POST - Add new student
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or 'name' not in data or 'roll' not in data or 'marks' not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_id = max([s["id"] for s in students], default=0) + 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "roll": data["roll"],
        "marks": data["marks"]
    }
    students.append(new_student)
    return jsonify(new_student), 201

# ✅ PUT - Update student by ID
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    for s in students:
        if s["id"] == student_id:
            s["name"] = data.get("name", s["name"])
            s["roll"] = data.get("roll", s["roll"])
            s["marks"] = data.get("marks", s["marks"])
            return jsonify(s)
    return jsonify({"error": "Student not found"}), 404

# ✅ DELETE - Remove student by ID
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Deleted"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import logging
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient("mongodb+srv://dornoy5:dornoy1583@new1.skezdm9.mongodb.net/")
db = client["school"]
students_collection = db["students"]

# Read - get all students
@app.route("/students", methods=["GET"])
def get_students():
    students = list(students_collection.find({}, {"_id": 0}))
    return jsonify(students)

# Create - add student
@app.route("/students", methods=["POST"])
def add_student():
    try:
        data = request.json
        logging.info(f"Received data: {data}")  # Log the received data

        if 'name' not in data:
            return jsonify({"error": "Missing student name"}), 400

        # Get the current maximum ID
        max_id_student = students_collection.find_one(sort=[("id", -1)])
        max_id = max_id_student['id'] if max_id_student else 0
        new_id = max_id + 1

        students_collection.insert_one({"id": new_id, "name": data['name']})
        return jsonify({"message": "Student added successfully", "id": new_id})

    except Exception as e:
        logging.error(f"Error occurred: {e}")  # Log the exception
        return jsonify({"error": str(e)}), 500
# Delete a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def del_students(student_id):
    result = students_collection.delete_one({"id": student_id})
    if result.deleted_count > 0:
        return jsonify({"message": f"Deleted student with ID {student_id}"})
    else:
        return jsonify({"message": "Student not found"}), 404

# Update a student
@app.route("/students/<int:student_id>", methods=["PUT"])
def upd_students(student_id):
    data = request.json
    result = students_collection.update_one({"id": student_id}, {"$set": data})
    if result.matched_count > 0:
        return jsonify({"message": f"Updated student with ID {student_id}"})
    else:
        return jsonify({"message": "Student not found"}), 404

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)

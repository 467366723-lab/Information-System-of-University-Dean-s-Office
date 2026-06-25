from flask import Blueprint, request, jsonify
from services import student_service
from models.student import Student

student_bp = Blueprint('student', __name__, url_prefix='/api/students')


# Get all students
@student_bp.route('', methods=['GET'])
def get_all_students():
    students = student_service.get_all_students()
    return jsonify([s.to_dict() for s in students]), 200


# Get a single student by ID
@student_bp.route('/<student_id>', methods=['GET'])
def get_student_by_id(student_id):
    student = student_service.get_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict()), 200


# Add a new student
@student_bp.route('', methods=['POST'])
def add_student():
    data = request.get_json()
    required_fields = ["student_id", "name", "grade"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: student_id, name, grade"}), 400

    if not isinstance(data["grade"], int) or data["grade"] <= 0:
        return jsonify({"error": "Grade must be a positive integer"}), 400

    student = Student(data["student_id"], data["name"], data["grade"])
    success = student_service.add_student(student)
    if not success:
        return jsonify({"error": "Student ID already exists"}), 409

    return jsonify(student.to_dict()), 201


# Update student info
@student_bp.route('/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()

    # Validate grade if provided
    if "grade" in data and (not isinstance(data["grade"], int) or data["grade"] <= 0):
        return jsonify({"error": "Grade must be a positive integer"}), 400

    success = student_service.update_student(
        student_id,
        new_name=data.get("name"),
        new_grade=data.get("grade")
    )
    if not success:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student updated successfully"}), 200


# Delete a student
@student_bp.route('/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    success = student_service.delete_student(student_id)
    if not success:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted successfully"}), 200
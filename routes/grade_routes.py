from flask import Blueprint, request, jsonify
from services import grade_service
from models.grade import Grade

grade_bp = Blueprint("grade", __name__, url_prefix="/api/grades")

@grade_bp.route("", methods=["GET"])
def get_all_grades():
    grades = grade_service.get_all_grades()
    return jsonify([g.to_dict() for g in grades]), 200

@grade_bp.route("", methods=["POST"])
def add_grade():
    data = request.get_json()
    required = ["student_id", "course_id", "score"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400
    if not isinstance(data["score"], int) or data["score"] < 0 or data["score"] > 100:
        return jsonify({"error": "Score must be between 0 and 100"}), 400
    new_grade = Grade(data["student_id"], data["course_id"], data["score"])
    ok = grade_service.add_grade(new_grade)
    if not ok:
        return jsonify({"error": "Grade record already exists"}), 409
    return jsonify(new_grade.to_dict()), 201

@grade_bp.route("/<student_id>/<course_id>", methods=["DELETE"])
def delete_grade(student_id, course_id):
    success = grade_service.delete_grade(student_id, course_id)
    if not success:
        return jsonify({"error": "Grade not found"}), 404
    return jsonify({"message": "Grade deleted successfully"}), 200
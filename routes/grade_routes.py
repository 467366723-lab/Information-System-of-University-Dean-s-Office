from flask import Blueprint, request, jsonify
from services import grade_service
from models.grade import Grade

grade_bp = Blueprint("grade", __name__, url_prefix="/api/grades")


# Get all grade records
@grade_bp.route("", methods=["GET"])
def get_all_grades():
    grades = grade_service.get_all_grades()
    return jsonify([g.to_dict() for g in grades]), 200


# Get grades by student ID
@grade_bp.route("/student/<student_id>", methods=["GET"])
def get_grade_by_student(student_id):
    res = grade_service.get_grades_by_student_id(student_id)
    return jsonify([g.to_dict() for g in res]), 200


# Get grades by course ID
@grade_bp.route("/course/<course_id>", methods=["GET"])
def get_grade_by_course(course_id):
    res = grade_service.get_grades_by_course_id(course_id)
    return jsonify([g.to_dict() for g in res]), 200


# Get student average score
@grade_bp.route("/avg/<student_id>", methods=["GET"])
def get_avg_score(student_id):
    avg = grade_service.calculate_student_average(student_id)
    return jsonify({
        "student_id": student_id,
        "average_score": avg,
        "message": "No grade records found" if avg is None else "Calculation successful"
    }), 200


# Add a new grade record
@grade_bp.route("", methods=["POST"])
def add_grade():
    data = request.get_json()
    required = ["student_id", "course_id", "score"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields: student_id, course_id, score"}), 400

    if not isinstance(data["score"], int):
        return jsonify({"error": "Score must be an integer"}), 400

    new_grade = Grade(data["student_id"], data["course_id"], data["score"])
    ok, msg = grade_service.add_grade(new_grade)
    if not ok:
        return jsonify({"error": msg}), 409
    return jsonify({"message": msg, "data": new_grade.to_dict()}), 201


# Update a grade record
@grade_bp.route('/<student_id>/<course_id>', methods=['PUT'])
def update_grade(student_id, course_id):
    data = request.get_json()
    if "score" not in data:
        return jsonify({"error": "Missing required field: score"}), 400

    if not isinstance(data["score"], int):
        return jsonify({"error": "Score must be an integer"}), 400

    if not (0 <= data["score"] <= 100):
        return jsonify({"error": "Score must be between 0 and 100"}), 400

    success = grade_service.update_grade(student_id, course_id, data["score"])
    if not success:
        return jsonify({"error": "Grade record not found"}), 404
    return jsonify({"message": "Grade updated successfully"}), 200


# Delete a grade record
@grade_bp.route('/<student_id>/<course_id>', methods=['DELETE'])
def delete_grade(student_id, course_id):
    success = grade_service.delete_grade(student_id, course_id)
    if not success:
        return jsonify({"error": "Grade record not found"}), 404
    return jsonify({"message": "Grade deleted successfully"}), 200
from flask import Blueprint, request, jsonify
from services import course_service
from models.course import Course

course_bp = Blueprint("course", __name__, url_prefix="/api/courses")


# Get all courses
@course_bp.route("", methods=["GET"])
def get_all_courses():
    courses = course_service.get_all_courses()
    return jsonify([c.to_dict() for c in courses]), 200


# Get a single course by ID
@course_bp.route("/<course_id>", methods=["GET"])
def get_course_by_id(course_id):
    course = course_service.get_course_by_id(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course.to_dict()), 200


# Add a new course
@course_bp.route("", methods=["POST"])
def add_course():
    data = request.get_json()
    required = ["course_id", "name", "credits"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields: course_id, name, credits"}), 400

    # Fix: Align credit validation with frontend (1-20)
    if not isinstance(data["credits"], int) or data["credits"] < 1 or data["credits"] > 20:
        return jsonify({"error": "Credits must be an integer between 1 and 20"}), 400

    new_course = Course(data["course_id"], data["name"], data["credits"])
    ok = course_service.add_course(new_course)
    if not ok:
        return jsonify({"error": "Course ID already exists"}), 409
    return jsonify(new_course.to_dict()), 201


# Update course info
@course_bp.route('/<course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()

    # Fix: Align credit validation with frontend (1-20)
    if "credits" in data and (not isinstance(data["credits"], int) or data["credits"] < 1 or data["credits"] > 20):
        return jsonify({"error": "Credits must be an integer between 1 and 20"}), 400

    success = course_service.update_course(
        course_id,
        new_name=data.get("name"),
        new_credits=data.get("credits")
    )
    if not success:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({"message": "Course updated successfully"}), 200


# Delete a course
@course_bp.route('/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    success = course_service.delete_course(course_id)
    if not success:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({"message": "Course deleted successfully"}), 200
from models.grade import Grade
from services.student_service import get_student_by_id
from services.course_service import get_course_by_id
import os

DATA_PATH = os.path.join("data", "grades.txt")


def _save_to_file(grade_list: list[Grade]):
    """Internal helper: write all grade data to file"""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        for g in grade_list:
            f.write(g.to_string() + "\n")


def get_all_grades() -> list[Grade]:
    """Get all grade records from the text file"""
    grades = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    grades.append(Grade.from_string(line))
    return grades


def get_grades_by_student_id(student_id: str) -> list[Grade]:
    """Get all grades for a specific student"""
    all_grades = get_all_grades()
    return [grade for grade in all_grades if grade.student_id == student_id]


def get_grades_by_course_id(course_id: str) -> list[Grade]:
    """Get all grades for a specific course"""
    all_grades = get_all_grades()
    return [g for g in all_grades if g.course_id == course_id]


def add_grade(grade: Grade) -> tuple[bool, str]:
    """
    Add a new grade record with validation.
    Returns (success: bool, message: str)
    """
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    # Validate student exists
    if not get_student_by_id(grade.student_id):
        return False, f"Student with ID {grade.student_id} does not exist"

    # Validate course exists
    if not get_course_by_id(grade.course_id):
        return False, f"Course with ID {grade.course_id} does not exist"

    # Validate score range
    if not (0 <= grade.score <= 100):
        return False, "Score must be between 0 and 100"

    # Validate no duplicate record
    all_grades = get_all_grades()
    for g in all_grades:
        if g.student_id == grade.student_id and g.course_id == grade.course_id:
            return False, "Grade record for this student and course already exists"

    # Write to file
    with open(DATA_PATH, 'a', encoding='utf-8') as file:
        file.write(grade.to_string() + '\n')
    return True, "Grade added successfully"


def calculate_student_average(student_id: str) -> float | None:
    """Calculate average score for a student, return None if no records"""
    student_grades = get_grades_by_student_id(student_id)
    if not student_grades:
        return None
    total_score = sum(g.score for g in student_grades)
    average = total_score / len(student_grades)
    return round(average, 2)


def update_grade(student_id: str, course_id: str, new_score: int) -> bool:
    """Update a grade record. Assumes score is already validated"""
    grades = get_all_grades()
    for g in grades:
        if g.student_id == student_id and g.course_id == course_id:
            g.score = new_score
            _save_to_file(grades)
            return True
    return False


def delete_grade(student_id: str, course_id: str) -> bool:
    """Delete a grade record by student ID and course ID"""
    grades = get_all_grades()
    new_grades = [g for g in grades if not (g.student_id == student_id and g.course_id == course_id)]
    if len(new_grades) == len(grades):
        return False
    _save_to_file(new_grades)
    return True
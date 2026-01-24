from models.grade import Grade
from services.student_service import get_student_by_id
from services.course_service import get_course_by_id
import os

DATA_PATH = os.path.join("data", "grades.txt")

def get_all_grades() -> list[Grade]:
    grades = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    grades.append(Grade.from_string(line))
    return grades

def get_grades_by_student_id(student_id: str) -> list[Grade]:
    """
    Get all grades of a specific student
    :param student_id: Target student ID
    :return: List of Grade objects for the student
    """
    all_grades = get_all_grades()
    student_grades = [grade for grade in all_grades if grade.student_id == student_id]
    return student_grades

def add_grade(grade: Grade) -> tuple[bool, str]:
    """
    Add a new grade (validate student and course existence)
    :param grade: Grade object to add
    :return: (Success status, Message)
    """
    # Validate student exists
    if not get_student_by_id(grade.student_id):
        return False, f"Student with ID {grade.student_id} does not exist"
    # Validate course exists
    if not get_course_by_id(grade.course_id):
        return False, f"Course with ID {grade.course_id} does not exist"
    # Validate score range (0-100)
    if not (0 <= grade.score <= 100):
        return False, "Score must be between 0 and 100"
    # Validate duplicate (same student + same course)
    all_grades = get_all_grades()
    for g in all_grades:
        if g.student_id == grade.student_id and g.course_id == grade.course_id:
            return False, "Duplicate grade for this student and course"
    # Add grade to file
    with open(DATA_PATH, 'a', encoding='utf-8') as file:
        file.write(grade.to_string() + '\n')
    return True, "Grade added successfully"

def calculate_student_average(student_id: str) -> float | None:
    """
    Calculate average score of a student
    :param student_id: Target student ID
    :return: Average score if grades exist, None otherwise
    """
    student_grades = get_grades_by_student_id(student_id)
    if not student_grades:
        return None
    total_score = sum(grade.score for grade in student_grades)
    average = total_score / len(student_grades)
    return round(average, 2)
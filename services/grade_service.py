from models.grade import Grade
import os

DATA_PATH = os.path.join("data", "grades.txt")

def _save_to_file(grade_list: list[Grade]):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        for grade in grade_list:
            f.write(grade.to_string() + "\n")

def get_all_grades() -> list[Grade]:
    grades = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                grade = Grade.from_string(line)
                if grade is not None:
                    grades.append(grade)
    return grades

def get_grade(student_id: str, course_id: str):
    grades = get_all_grades()
    for grade in grades:
        if grade.student_id == student_id and grade.course_id == course_id:
            return grade
    return None

def add_grade(grade: Grade) -> bool:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if get_grade(grade.student_id, grade.course_id):
        return False
    with open(DATA_PATH, 'a', encoding='utf-8') as file:
        file.write(grade.to_string() + '\n')
    return True

def delete_grade(student_id: str, course_id: str) -> bool:
    grades = get_all_grades()
    new_grades = [g for g in grades if not (g.student_id == student_id and g.course_id == course_id)]
    if len(new_grades) == len(grades):
        return False
    _save_to_file(new_grades)
    return True
from models.student import Student
import os

DATA_PATH = os.path.join("data", "students.txt")


def _save_to_file(student_list: list[Student]):
    """Internal helper: write all student data to file"""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        for stu in student_list:
            f.write(stu.to_string() + "\n")


def get_all_students() -> list[Student]:
    """Get all students from the text file"""
    students = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    students.append(Student.from_string(line))
    return students


def get_student_by_id(student_id: str) -> Student | None:
    """Get a single student by ID, return None if not found"""
    students = get_all_students()
    for student in students:
        if student.student_id == student_id:
            return student
    return None


def add_student(student: Student) -> bool:
    """Add a new student. Return False if ID already exists"""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if get_student_by_id(student.student_id):
        return False
    with open(DATA_PATH, 'a', encoding='utf-8') as file:
        file.write(student.to_string() + '\n')
    return True


def update_student(student_id: str, new_name: str | None = None, new_grade: int | None = None) -> bool:
    """Update student info by ID. Return False if student not found"""
    students = get_all_students()
    for s in students:
        if s.student_id == student_id:
            if new_name is not None:
                s.name = new_name
            if new_grade is not None:
                s.grade = new_grade
            _save_to_file(students)
            return True
    return False


def delete_student(student_id: str) -> bool:
    """Delete a student by ID. Return False if student not found"""
    students = get_all_students()
    new_students = [s for s in students if s.student_id != student_id]
    if len(new_students) == len(students):
        return False
    _save_to_file(new_students)
    return True
from models.student import Student
import os

# Path to the student data file
DATA_PATH = os.path.join("data", "students.txt")

def get_all_students() -> list[Student]:
    """
    Get all students from the text file
    :return: List of Student objects
    """
    students = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    students.append(Student.from_string(line))
    return students

def get_student_by_id(student_id: str) -> Student | None:
    """
    Get a student by their ID
    :param student_id: Target student ID
    :return: Student object if found, None otherwise
    """
    students = get_all_students()
    for student in students:
        if student.student_id == student_id:
            return student
    return None

def add_student(student: Student) -> bool:
    """
    Add a new student to the text file (avoid duplicate ID)
    :param student: Student object to add
    :return: True if added successfully, False if ID already exists
    """
    if get_student_by_id(student.student_id):
        return False  # Duplicate student ID
    with open(DATA_PATH, 'a', encoding='utf-8') as file:
        file.write(student.to_string() + '\n')
    return True
from models.course import Course
import os

DATA_PATH = os.path.join("data", "courses.txt")

def get_all_courses() -> list[Course]:
    courses = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    courses.append(Course.from_string(line))
    return courses

def get_course_by_id(course_id: str) -> Course | None:
    courses = get_all_courses()
    for course in courses:
        if course.course_id == course_id:
            return course
    return None

def add_course(course: Course) -> bool:
    if get_course_by_id(course.course_id):
        return False
    with open(DATA_PATH, 'a', encoding='utf-8') as file:
        file.write(course.to_string() + '\n')
    return True
from models.course import Course
import os

DATA_PATH = os.path.join("data", "courses.txt")


def _save_to_file(course_list: list[Course]):
    """Internal helper: write all course data to file"""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        for course in course_list:
            f.write(course.to_string() + "\n")


def get_all_courses() -> list[Course]:
    """Get all courses from the text file"""
    courses = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    courses.append(Course.from_string(line))
    return courses


def get_course_by_id(course_id: str) -> Course | None:
    """Get a single course by ID, return None if not found"""
    courses = get_all_courses()
    for course in courses:
        if course.course_id == course_id:
            return course
    return None


def add_course(course: Course) -> bool:
    """Add a new course. Return False if ID already exists"""
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if get_course_by_id(course.course_id):
        return False
    with open(DATA_PATH, 'a', encoding='utf-8') as file:
        file.write(course.to_string() + '\n')
    return True


def update_course(course_id: str, new_name: str | None = None, new_credits: int | None = None) -> bool:
    """Update course info by ID. Return False if course not found"""
    courses = get_all_courses()
    for c in courses:
        if c.course_id == course_id:
            if new_name is not None:
                c.name = new_name
            if new_credits is not None:
                c.credits = new_credits
            _save_to_file(courses)
            return True
    return False


def delete_course(course_id: str) -> bool:
    """Delete a course by ID. Return False if course not found"""
    courses = get_all_courses()
    new_courses = [c for c in courses if c.course_id != course_id]
    if len(new_courses) == len(courses):
        return False
    _save_to_file(new_courses)
    return True
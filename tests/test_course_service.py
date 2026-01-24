import unittest
import os
from models.course import Course
from services.course_service import get_all_courses, get_course_by_id, add_course

TEST_DATA_PATH = os.path.join("data", "courses_test.txt")

class TestCourseService(unittest.TestCase):
    def setUp(self):
        import services.course_service
        services.course_service.DATA_PATH = TEST_DATA_PATH
        with open(TEST_DATA_PATH, 'w', encoding='utf-8') as file:
            file.write("C001,Math,4\nC002,English,2\n")

    def tearDown(self):
        if os.path.exists(TEST_DATA_PATH):
            os.remove(TEST_DATA_PATH)

    def test_get_all_courses(self):
        courses = get_all_courses()
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].course_id, "C001")
        self.assertEqual(courses[1].name, "English")

    def test_get_course_by_id_exist(self):
        course = get_course_by_id("C001")
        self.assertIsNotNone(course)
        self.assertEqual(course.credits, 4)

    def test_get_course_by_id_not_exist(self):
        course = get_course_by_id("C003")
        self.assertIsNone(course)

    def test_add_course_success(self):
        new_course = Course("C003", "Computer Science", 3)
        success = add_course(new_course)
        self.assertTrue(success)
        self.assertEqual(len(get_all_courses()), 3)

    def test_add_course_duplicate_id(self):
        duplicate_course = Course("C001", "Advanced Math", 4)
        success = add_course(duplicate_course)
        self.assertFalse(success)
        self.assertEqual(len(get_all_courses()), 2)

if __name__ == "__main__":
    unittest.main()
import unittest
import os
from models.grade import Grade
from services.grade_service import add_grade, calculate_student_average
from services.student_service import add_student
from services.course_service import add_course
from models.student import Student
from models.course import Course

TEST_STUDENT_PATH = os.path.join("data", "students_test.txt")
TEST_COURSE_PATH = os.path.join("data", "courses_test.txt")
TEST_GRADE_PATH = os.path.join("data", "grades_test.txt")

class TestGradeService(unittest.TestCase):
    def setUp(self):
        # Override data paths for testing
        import services.student_service
        import services.course_service
        import services.grade_service
        services.student_service.DATA_PATH = TEST_STUDENT_PATH
        services.course_service.DATA_PATH = TEST_COURSE_PATH
        services.grade_service.DATA_PATH = TEST_GRADE_PATH

        # Add test students and courses
        add_student(Student("S001", "Alice", 2022))
        add_student(Student("S002", "Bob", 2023))
        add_course(Course("C001", "Math", 4))
        add_course(Course("C002", "English", 2))

    def tearDown(self):
        # Clean up test files
        for path in [TEST_STUDENT_PATH, TEST_COURSE_PATH, TEST_GRADE_PATH]:
            if os.path.exists(path):
                os.remove(path)

    def test_add_grade_success(self):
        """Test adding a valid grade"""
        grade = Grade("S001", "C001", 90.5)
        success, message = add_grade(grade)
        self.assertTrue(success)
        self.assertEqual(message, "Grade added successfully")

    def test_add_grade_invalid_student(self):
        """Test adding grade for non-existing student"""
        grade = Grade("S003", "C001", 85)
        success, message = add_grade(grade)
        self.assertFalse(success)
        self.assertIn("does not exist", message)

    def test_add_grade_invalid_course(self):
        """Test adding grade for non-existing course"""
        grade = Grade("S001", "C003", 85)
        success, message = add_grade(grade)
        self.assertFalse(success)
        self.assertIn("does not exist", message)

    def test_add_grade_invalid_score(self):
        """Test adding grade with score out of range"""
        grade = Grade("S001", "C001", 105)
        success, message = add_grade(grade)
        self.assertFalse(success)
        self.assertIn("between 0 and 100", message)

    def test_calculate_average(self):
        """Test calculating student average score"""
        # Add two grades for S001
        add_grade(Grade("S001", "C001", 90))
        add_grade(Grade("S001", "C002", 80))
        average = calculate_student_average("S001")
        self.assertEqual(average, 85.0)

    def test_calculate_average_no_grades(self):
        """Test calculating average when no grades exist"""
        average = calculate_student_average("S002")
        self.assertIsNone(average)

if __name__ == "__main__":
    unittest.main()
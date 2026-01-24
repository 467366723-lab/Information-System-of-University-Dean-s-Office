import unittest
import os
from models.student import Student
from services.student_service import get_all_students, get_student_by_id, add_student

# Test data path (use a test file to avoid affecting real data)
TEST_DATA_PATH = os.path.join("data", "students_test.txt")

class TestStudentService(unittest.TestCase):
    def setUp(self):
        """Run before each test case (prepare test data)"""
        # Override the data path for testing
        import services.student_service
        services.student_service.DATA_PATH = TEST_DATA_PATH
        # Create test file with sample data
        with open(TEST_DATA_PATH, 'w', encoding='utf-8') as file:
            file.write("S001,Alice,2022\nS002,Bob,2023\n")

    def tearDown(self):
        """Run after each test case (clean up test data)"""
        if os.path.exists(TEST_DATA_PATH):
            os.remove(TEST_DATA_PATH)

    def test_get_all_students(self):
        """Test getting all students"""
        students = get_all_students()
        self.assertEqual(len(students), 2)
        self.assertEqual(students[0].student_id, "S001")
        self.assertEqual(students[1].name, "Bob")

    def test_get_student_by_id_exist(self):
        """Test getting an existing student by ID"""
        student = get_student_by_id("S001")
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Alice")

    def test_get_student_by_id_not_exist(self):
        """Test getting a non-existing student by ID"""
        student = get_student_by_id("S003")
        self.assertIsNone(student)

    def test_add_student_success(self):
        """Test adding a new student successfully"""
        new_student = Student("S003", "Charlie", 2024)
        success = add_student(new_student)
        self.assertTrue(success)
        self.assertEqual(len(get_all_students()), 3)

    def test_add_student_duplicate_id(self):
        """Test adding a student with duplicate ID"""
        duplicate_student = Student("S001", "Alice Duplicate", 2022)
        success = add_student(duplicate_student)
        self.assertFalse(success)
        self.assertEqual(len(get_all_students()), 2)

if __name__ == "__main__":
    unittest.main()
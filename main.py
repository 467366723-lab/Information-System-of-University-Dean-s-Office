from models.student import Student
from models.course import Course
from models.grade import Grade
from services import student_service, course_service, grade_service


def display_menu() -> None:
    """Display the main menu of the system"""
    print("\n===== University Dean's Office Information System =====")
    print("1. Student Management")
    print("2. Course Management")
    print("3. Grade Management")
    print("4. Exit")
    print("======================================================")


def student_management_menu() -> None:
    print("\n----- Student Management -----")
    print("1. View all students")
    print("2. Search student by ID")
    print("3. Add new student")
    print("4. Return to main menu")


def course_management_menu() -> None:
    print("\n----- Course Management -----")
    print("1. View all courses")
    print("2. Search course by ID")
    print("3. Add new course")
    print("4. Return to main menu")


def grade_management_menu() -> None:
    print("\n----- Grade Management -----")
    print("1. View all grades")
    print("2. Search grades by student ID")
    print("3. Add new grade")
    print("4. Calculate student average score")
    print("5. Return to main menu")


def main() -> None:
    while True:
        display_menu()
        choice = input("Please enter your choice (1-4): ")

        # Student Management
        if choice == "1":
            while True:
                student_management_menu()
                sub_choice = input("Please enter your choice (1-4): ")
                if sub_choice == "1":
                    students = student_service.get_all_students()
                    if not students:
                        print("No students found.")
                    else:
                        print(f"{'Student ID':<10} {'Name':<20} {'Grade'}")
                        print("-" * 40)
                        for s in students:
                            print(f"{s.student_id:<10} {s.name:<20} {s.grade}")
                elif sub_choice == "2":
                    student_id = input("Enter student ID to search: ")
                    student = student_service.get_student_by_id(student_id)
                    if student:
                        print(f"\nStudent Found:")
                        print(f"ID: {student.student_id}")
                        print(f"Name: {student.name}")
                        print(f"Grade: {student.grade}")
                    else:
                        print(f"Student with ID {student_id} not found.")
                elif sub_choice == "3":
                    student_id = input("Enter student ID (e.g., S004): ")
                    name = input("Enter student name (e.g., David Wilson): ")
                    grade = input("Enter enrollment grade (e.g., 2024): ")
                    # Validate grade is integer
                    if not grade.isdigit():
                        print("Error: Grade must be a number.")
                        continue
                    # Create student object
                    student = Student(student_id, name, int(grade))
                    success = student_service.add_student(student)
                    if success:
                        print("Student added successfully.")
                    else:
                        print(f"Error: Student with ID {student_id} already exists.")
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")

        # Course Management
        elif choice == "2":
            while True:
                course_management_menu()
                sub_choice = input("Please enter your choice (1-4): ")
                if sub_choice == "1":
                    courses = course_service.get_all_courses()
                    if not courses:
                        print("No courses found.")
                    else:
                        # 第1处修改：Credits → Course Credits（仅显示，非变量）
                        print(f"{'Course ID':<10} {'Name':<30} {'Course Credits'}")
                        print("-" * 50)
                        for c in courses:
                            print(f"{c.course_id:<10} {c.name:<30} {c.credits}")
                elif sub_choice == "2":
                    course_id = input("Enter course ID to search: ")
                    course = course_service.get_course_by_id(course_id)
                    if course:
                        print(f"\nCourse Found:")
                        print(f"ID: {course.course_id}")
                        print(f"Name: {course.name}")
                        # 第2处修改：Credits → Course Credits（仅显示，非变量）
                        print(f"Course Credits: {course.credits}")
                    else:
                        print(f"Course with ID {course_id} not found.")
                elif sub_choice == "3":
                    course_id = input("Enter course ID (e.g., C004): ")
                    name = input("Enter course name (e.g., Data Structures): ")
                    # 核心修改：变量名 credits → course_credits（第3处，消除警告的关键）
                    course_credits = input("Enter course credits (e.g., 3): ")
                    if not course_credits.isdigit():
                        print("Error: Course credits must be a number.")
                        continue
                    course = Course(course_id, name, int(course_credits))
                    success = course_service.add_course(course)
                    if success:
                        print("Course added successfully.")
                    else:
                        print(f"Error: Course with ID {course_id} already exists.")
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")

        # Grade Management
        elif choice == "3":
            while True:
                grade_management_menu()
                sub_choice = input("Please enter your choice (1-5): ")
                if sub_choice == "1":
                    grades = grade_service.get_all_grades()
                    if not grades:
                        print("No grades found.")
                    else:
                        print(f"{'Student ID':<10} {'Course ID':<10} {'Score'}")
                        print("-" * 35)
                        for g in grades:
                            print(f"{g.student_id:<10} {g.course_id:<10} {g.score:.1f}")
                elif sub_choice == "2":
                    student_id = input("Enter student ID to search grades: ")
                    grades = grade_service.get_grades_by_student_id(student_id)
                    if not grades:
                        print(f"No grades found for student {student_id}.")
                    else:
                        print(f"\nGrades for Student {student_id}:")
                        print(f"{'Course ID':<10} {'Score'}")
                        print("-" * 20)
                        for g in grades:
                            print(f"{g.course_id:<10} {g.score:.1f}")
                elif sub_choice == "3":
                    student_id = input("Enter student ID: ")
                    course_id = input("Enter course ID: ")
                    score = input("Enter score (0-100): ")
                    # Validate score is a number
                    try:
                        score = float(score)
                    except ValueError:
                        print("Error: Score must be a number.")
                        continue
                    grade = Grade(student_id, course_id, score)
                    success, message = grade_service.add_grade(grade)
                    print(message)
                elif sub_choice == "4":
                    student_id = input("Enter student ID to calculate average: ")
                    average = grade_service.calculate_student_average(student_id)
                    if average is None:
                        print(f"No grades found for student {student_id}, cannot calculate average.")
                    else:
                        print(f"Average score of student {student_id}: {average}")
                elif sub_choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")

        # Exit
        elif choice == "4":
            print("Thank you for using the system. Goodbye!")
            break

        # Invalid main choice
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
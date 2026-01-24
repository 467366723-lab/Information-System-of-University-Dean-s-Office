class Student:
    def __init__(self, student_id: str, name: str, grade: int):
        """
        Initialize a Student object
        :param student_id: Unique identifier of the student (e.g., S001)
        :param name: Full name of the student
        :param grade: Enrollment grade (e.g., 2022)
        """
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_string(self) -> str:
        """Convert student object to string (for writing to text file)"""
        return f"{self.student_id},{self.name},{self.grade}"

    @staticmethod
    def from_string(line: str) -> 'Student':
        """Create student object from text file line"""
        parts = line.strip().split(',')
        return Student(parts[0], parts[1], int(parts[2]))
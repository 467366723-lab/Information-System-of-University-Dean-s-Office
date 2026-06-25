class Grade:
    def __init__(self, student_id: str, course_id: str, score: float):
        """
        Initialize a Grade object
        :param student_id: ID of the student
        :param course_id: ID of the course
        :param score: Score of the student in the course (0-100)
        """
        self.student_id = student_id
        self.course_id = course_id
        self.score = score

    def to_string(self) -> str:
        return f"{self.student_id},{self.course_id},{self.score:.1f}"

    @staticmethod
    def from_string(line: str) -> 'Grade':
        parts = line.strip().split(',')
        return Grade(parts[0], parts[1], float(parts[2]))

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "course_id": self.course_id,
            "score": round(self.score, 1)
        }
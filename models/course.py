class Course:
    def __init__(self, course_id: str, name: str, credits: int):
        """
        Initialize a Course object
        :param course_id: Unique identifier of the course (e.g., C001)
        :param name: Name of the course
        :param credits: Number of credits for the course
        """
        self.course_id = course_id
        self.name = name
        self.credits = credits

    def to_string(self) -> str:
        return f"{self.course_id},{self.name},{self.credits}"

    @staticmethod
    def from_string(line: str) -> 'Course':
        parts = line.strip().split(',')
        return Course(parts[0], parts[1], int(parts[2]))

    def to_dict(self) -> dict:
        return {
            "course_id": self.course_id,
            "name": self.name,
            "credits": self.credits
        }
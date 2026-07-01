class Grade:
    def __init__(self, student_id: str, course_id: str, score: int):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score

    def to_string(self) -> str:
        return f"{self.student_id},{self.course_id},{self.score}"

    @classmethod
    def from_string(cls, line: str):
        line = line.strip()
        if not line:
            return None
        parts = line.split(",")
        if len(parts) != 3:
            return None
        try:
            score = int(parts[2])
        except ValueError:
            return None
        return cls(parts[0], parts[1], score)

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "course_id": self.course_id,
            "score": self.score
        }
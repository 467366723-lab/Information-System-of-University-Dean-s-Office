class Course:
    def __init__(self, course_id: str, name: str, credits: int):
        self.course_id = course_id
        self.name = name
        self.credits = credits

    def to_string(self) -> str:
        return f"{self.course_id},{self.name},{self.credits}"

    @classmethod
    def from_string(cls, line: str):
        line = line.strip()
        if not line:
            return None
        parts = line.split(",")
        if len(parts) != 3:
            return None
        try:
            credits = int(parts[2])
        except ValueError:
            return None
        return cls(parts[0], parts[1], credits)

    def to_dict(self) -> dict:
        return {
            "course_id": self.course_id,
            "name": self.name,
            "credits": self.credits
        }
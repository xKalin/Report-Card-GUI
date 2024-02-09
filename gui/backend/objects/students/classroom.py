import settings
import json


class Classroom:

    def __init__(self):
        self._path = settings.STUDENTS_JSON_PATH
        self.students = self.load_students()

    def load_students(self):
        with open(self._path) as f:
            data = json.load(f)
        return data

    def save_students(self, student_data):
        with open(self._path, "w") as f:
            json.dump(student_data, fp=f, ensure_ascii=False, indent=4)

    def add_student(self, student):
        self.students.append(student.serialize_student)



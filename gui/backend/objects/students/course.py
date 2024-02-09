import settings
import json

from gui.backend.objects.students.student import Students


class Course:

    def __init__(self):
        self._path = settings.STUDENTS_JSON_PATH
        self.students = self.load_students()

    def load_students(self):
        with open(self._path) as f:
            data = json.load(f)
        return data

    def validate_students_from_df(self, df):
        student_names = self.students.keys()
        new_students = df[~df['Name'].isin(student_names)]
        self.__enroll(new_students)
        self.save_students_json()

    def save_students_json(self):
        with open(self._path, "w") as f:
            json.dump(self.students, fp=f, ensure_ascii=False, indent=4)

    def is_enrolled(self, name):
        return True if name in self.students else False

    def __enroll(self, new_students):
        Students().add_students(self.students, new_students)





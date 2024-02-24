import json

import settings
from gui.backend.calculator.final_grade_calculator import FinalGradeCalculator
from gui.backend.objects.assessments import Assessments
from gui.backend.objects.student import Students

student_json_path = settings.STUDENTS_JSON_PATH


class Course:
    def __init__(self):
        self.students = self.__load_students()
        self.Assessment = Assessments()
        self.subject = self.get_default_subject()
        self.Assessment_list, self.Properties_list = self.Assessment.get_assessments(self.subject)

    @staticmethod
    def __load_students():
        with open(student_json_path) as f:
            data = json.load(f)
        return data

    def get_students(self):
        return self.students[self.subject]

    def save_students_json(self):
        with open(student_json_path, "w") as f:
            json.dump(self.students, fp=f, ensure_ascii=False, indent=4)

    def validate_students_from_excel(self, df):
        student_names = self.students.keys()
        new_students = df[~df['Name'].isin(student_names)]
        self.__enroll(new_students)
        self.save_students_json()

    def is_enrolled(self, name):
        return True if name in self.students else False

    def __enroll(self, new_students):
        Students().add_students(self.students[self.subject], new_students)

    def calculate_final_grade(self):
        final_cal = FinalGradeCalculator(self.Assessment.assessments, self.Assessment.assessments_property)
        student_roster = self.students[self.subject]
        for student in student_roster.keys():
            student_data = student_roster[student]
            final_grade, assessments = final_cal.calculate(student)
            student_data['Final Grade'] = final_grade
            student_data['Assessments'] = assessments
        self.save_students_json()

    def get_default_subject(self):
        default_subject = self.Assessment.assessments_json.keys()
        if len(default_subject) == 0:
            self.new_course('Language')
            return 'Language'
        return list(default_subject)[0]

    def select_subject(self, subject):
        self.subject = subject
        self.Assessment_list, self.Properties_list = self.Assessment.get_assessments(self.subject)

    def new_course(self, subject):
        self.Assessment.assessments_json[subject] = {}
        self.Assessment.assessments_property_json[subject] = {}
        self.Assessment.save_assessments_json()
        self.students[subject] = {}
        self.save_students_json()
        self.select_subject(subject)

    def delete_course(self, subject):
        del self.Assessment.assessments_json[subject]
        del self.Assessment.assessments_property_json[subject]
        self.Assessment.save_assessments_json()
        del self.students[subject]
        self.save_students_json()

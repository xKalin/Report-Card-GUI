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
        self.assessments, self.properties = self.Assessment.get_assessments(self.subject)

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

    def validate_new_student(self, new_student):
        classroom = self.get_students()
        classroom[new_student] = {}
        self.Assessment.add_new_student(new_student)
        self.calculate_final_grade()
        self.Assessment.save_assessments_json()

    def delete_student(self, student):
        del self.get_students()[student]
        for name, assessment in self.Assessment.assessments.items():
            index = next((index for (index, d) in enumerate(assessment) if d["Name"] == student), None)
            del assessment[index]
        self.save_all()

    def is_enrolled(self, name):
        return True if name in self.students else False

    def __enroll(self, new_students):
        Students().add_students(self.get_students(), new_students)

    def calculate_final_grade(self):
        final_cal = FinalGradeCalculator(self.assessments, self.properties)
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
        self.assessments, self.properties = self.Assessment.get_assessments(subject)

    def new_course(self, subject):
        self.Assessment.assessments_json[subject] = {}
        self.Assessment.assessments_property_json[subject] = {}
        self.students[subject] = {}
        self.save_all()
        self.select_subject(subject)

    def delete_course(self, subject):
        del self.Assessment.assessments_json[subject]
        del self.Assessment.assessments_property_json[subject]
        del self.students[subject]
        self.save_all()

    def save_all(self):
        self.save_students_json()
        self.Assessment.save_assessments_json()

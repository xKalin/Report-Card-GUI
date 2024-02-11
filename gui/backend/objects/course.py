import settings
import json

from gui.backend.calculator.final_grade_calculator import FinalGradeCalculator
from gui.backend.objects.assessments import Assessments
from gui.backend.objects.student import Students
from gui.popup import init_course_popup

student_json_path = settings.STUDENTS_JSON_PATH
course_json_path = settings.COURSE_JSON_PATH


class Course:
    def __init__(self):
        self.course = self.__load_course()
        self.selected_course = self.get_subject()
        self.students = self.__load_students()
        self.Assessment = Assessments(self.selected_course)

    @staticmethod
    def __load_students():
        with open(student_json_path) as f:
            data = json.load(f)
        return data

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
        Students().add_students(self.students, new_students)

    def calculate_final_grade(self):
        final_cal = FinalGradeCalculator(self.Assessment.assessments, self.Assessment.assessments_property)
        for student in self.students.keys():
            student_data = self.students[student]
            final_grade, assessments = final_cal.calculate(student)
            student_data['Final Grade'] = final_grade
            student_data['Assessments'] = assessments
        self.save_students_json()

    @staticmethod
    def __load_course():
        with open(course_json_path) as f:
            data = json.load(f)
        return data

    def save_course_json(self):
        with open(course_json_path, "w") as f:
            json.dump(self.course, fp=f, ensure_ascii=False, indent=4)

    def get_subject(self):
        courses = self.course['Courses']
        if len(courses) == 0:
            init_course_popup(self)
        return courses[0]

    def select_subject(self, subject):
        self.selected_course = subject

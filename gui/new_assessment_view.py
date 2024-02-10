from tkinter import StringVar

from gui.backend.objects.assessments.Assessments import Assessments
from gui.backend.objects.students.course import Course
import customtkinter as ctk

from gui.tkinter_utils import save_data


def new_assessment_view(self, assessment_name):
    # Load default template
    course = Course()
    assessment = Assessments()

    self.main_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform="equal")
    data = {}
    old_title = assessment_name

    # Title Bar
    label = ctk.CTkLabel(self.main_frame, text="Assessment : ", font=ctk.CTkFont(size=14, weight="bold"))
    label.grid(row=0, column=0, padx=0, pady=5)
    title = StringVar(self.main_frame, value=old_title)
    data["Assessment"] = title
    entry = ctk.CTkEntry(self.main_frame, textvariable=title, width=240)
    entry.grid(row=0, column=1, padx=0, pady=5)

    save_button = ctk.CTkButton(self.main_frame, text='Save',
                                command=(lambda frame=self:
                                         save_data(frame, old_title, data)))

    save_button.grid(row=0, column=8)
    # Body
    records = []
    data['df'] = records

    column = 0
    columns = assessment.get_assessment_columns()
    for column_name in columns:
        label = ctk.CTkLabel(self.main_frame, text=column_name, font=ctk.CTkFont(size=12, weight="bold"))
        label.grid(row=1, column=column, padx=20, pady=(20, 10))
        column += 1

    students = course.load_students().keys()
    row = 3
    for student in students:
        row_data = {}

        student_name = ctk.CTkTextbox(self.main_frame, height=20, width=120)
        student_name.insert("0.0", student)
        student_name.grid(row=row, column=0, padx=10, pady=8)
        student_name.configure(state='disable')
        row_data['Name'] = student

        for column in columns[1:]:
            print(column)
        records.append(row_data)
        row += 1


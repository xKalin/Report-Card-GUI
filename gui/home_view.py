from tkinter import StringVar

import customtkinter as ctk

from gui.popup import new_assessment_popup, delete_assessment_popup
from gui.tkinter_utils import previous_button


def home_view(self, page=0):
    # Configuration
    self.main_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform="equal")

    previous_page = ctk.CTkButton(self.main_frame, text='Previous', command=lambda val=self: previous_button(val, page))
    previous_page.grid(row=0, column=0, pady=10, padx=10)

    next_page = ctk.CTkButton(self.main_frame, text='Next')
    next_page.grid(row=0, column=1, pady=10, padx=10)

    new_assignment_button = ctk.CTkButton(self.main_frame, text='New Assessment',
                                          command=lambda frame=self: new_assessment_popup(frame))
    new_assignment_button.grid(row=0, column=2, pady=8)

    delete_assessment_button = ctk.CTkButton(self.main_frame, text='Delete Assessment',
                                             command=lambda frame=self: delete_assessment_popup(frame))
    delete_assessment_button.grid(row=0, column=3, pady=8)

    add_student = ctk.CTkButton(self.main_frame, text='Add Student')
    add_student.grid(row=0, column=4, pady=10, padx=10)

    delete_student = ctk.CTkButton(self.main_frame, text='Delete Student')
    delete_student.grid(row=0, column=5, pady=10, padx=10)

    # Body
    course = self.Course
    course.calculate_final_grade()

    column_index = 1
    assessments = course.Assessment.get_assessment_names()
    for column_name in assessments:
        label = ctk.CTkLabel(self.main_frame, text=column_name, font=ctk.CTkFont(size=12, weight="bold"))
        label.grid(row=1, column=column_index, padx=20, pady=(20, 10))
        column_index += 1

    # Final Grade column
    label = ctk.CTkLabel(self.main_frame, text='Final Grade', font=ctk.CTkFont(size=12, weight="bold"))
    label.grid(row=1, column=column_index, padx=20, pady=(20, 10))
    column_index += 1

    student_json = course.get_students()
    row_index = 2
    for student, student_data in student_json.items():
        student_button = ctk.CTkButton(self.main_frame, text=student, width=120,
                                          fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        student_button.grid(row=row_index, column=0, padx=10, pady=10)
        column_index = 1

        assessments = student_data['Assessments']

        for value in assessments.values():
            text = StringVar(self.main_frame, value=value['Grade'])
            input_box = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
            input_box.grid(row=row_index, column=column_index, pady=8)
            input_box.configure(state='disable')
            column_index += 1

        final_grade = student_data['Final Grade']
        text = StringVar(self.main_frame, value=final_grade)
        input_box = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
        input_box.grid(row=row_index, column=column_index, pady=8)
        input_box.configure(state='disable')

        row_index += 1






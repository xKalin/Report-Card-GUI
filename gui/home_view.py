from tkinter import StringVar

import customtkinter as ctk

from gui.popup import new_assessment_popup, delete_assessment_popup, add_student_popup, delete_student_popup
from gui.tkinter_utils import previous_button, next_button, download_button


def home_view(self, page):
    course = self.Course
    course.calculate_final_grade()

    per_page = 5
    start = per_page * page
    end = per_page * page + per_page

    # Configuration
    self.main_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform="equal")

    previous_page = ctk.CTkButton(self.main_frame, text='Previous', command=lambda val=self: previous_button(val, page))
    previous_page.grid(row=0, column=0, pady=10, padx=10)

    next_page = ctk.CTkButton(self.main_frame, text='Next',
                              command=lambda val=self: next_button(val, page, len(self.Course.assessments)))
    next_page.grid(row=0, column=1, pady=10, padx=10)

    new_assignment_button = ctk.CTkButton(self.main_frame, text='New Assessment',
                                          command=lambda frame=self: new_assessment_popup(frame))
    new_assignment_button.grid(row=0, column=2, pady=10, padx=10)

    delete_assessment_button = ctk.CTkButton(self.main_frame, text='Delete Assessment',
                                             command=lambda frame=self: delete_assessment_popup(frame))
    delete_assessment_button.grid(row=0, column=3, pady=10, padx=10)

    add_student = ctk.CTkButton(self.main_frame, text='Add Student',
                                command=lambda app=self: add_student_popup(app))
    add_student.grid(row=0, column=4, pady=10, padx=10)

    delete_student = ctk.CTkButton(self.main_frame, text='Delete Student',
                                   command=lambda app=self: delete_student_popup(app))
    delete_student.grid(row=0, column=5, pady=10, padx=10)

    excel_button = ctk.CTkButton(self.main_frame, text='Download', command=lambda frame=self: download_button(frame))
    excel_button.grid(row=0, column=6, pady=10, padx=10)

    # Body

    column_index = 1
    assessments = list(course.Assessment.get_assessment_names())[start:end]
    for column_name in assessments:
        label = ctk.CTkLabel(self.main_frame, text=column_name, font=ctk.CTkFont(size=12, weight="bold"))
        label.grid(row=1, column=column_index, padx=20, pady=(20, 10))
        column_index += 1

    # Final Grade column
    label = ctk.CTkLabel(self.main_frame, text='Final Grade', font=ctk.CTkFont(size=12, weight="bold"))
    label.grid(row=1, column=column_index, padx=20, pady=(20, 10))
    column_index += 1

    student_json = course.get_students()
    student_json = sorted(student_json.items(), key=lambda val: val[0].split()[-1])
    row_index = 2
    for student, student_data in student_json:
        var = StringVar(self.main_frame, value=student)
        student_button = ctk.CTkButton(self.main_frame, text=student, width=120,
                                       command=lambda val=var.get(): self.load_student_view(val),
                                       fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        student_button.grid(row=row_index, column=0, padx=10, pady=10)
        column_index = 1

        assessments = list(student_data['Assessments'].items())
        for name, value in assessments[start:end]:
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

from tkinter import StringVar

import customtkinter as ctk

from gui.tkinter_utils import save_data


def new_assessment_view(self, assessment_name):
    # Load default template
    course = self.Course
    assessment = course.Assessment

    self.main_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7), weight=1, uniform="equal")
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

    save_button.grid(row=0, column=8, pady=10, padx=10)
    # Body
    records = []
    data['df'] = records

    column_index = 0
    columns = assessment.get_assessment_columns()
    for column_name in columns:
        label = ctk.CTkLabel(self.main_frame, text=column_name, font=ctk.CTkFont(size=12, weight="bold"))
        label.grid(row=1, column=column_index, padx=20, pady=(20, 10))
        column_index += 1

    students = course.students.keys()
    row_index = 3
    for student in students:
        row_data = {}

        student_name = ctk.CTkTextbox(self.main_frame, height=20, width=120)
        student_name.insert("0.0", student)
        student_name.grid(row=row_index, column=0, padx=10, pady=8)
        student_name.configure(state='disable')
        row_data['Name'] = student

        column_index = 1
        for column in columns[1:]:
            text = StringVar(self.main_frame, value='')
            input_box = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
            input_box.grid(row=row_index, column=column_index, padx=0, pady=8)
            row_data[column] = text
            column_index += 1
        records.append(row_data)
        row_index += 1

    properties_default = assessment.get_default_properties()
    properties = {}
    data['properties'] = properties
    row_index = 3

    for text, val in properties_default.items():
        label = ctk.CTkLabel(self.main_frame, text=text, font=ctk.CTkFont(size=12, weight="bold"))
        label.grid(row=row_index, column=7, padx=20, pady=(20, 10))

        if text == "Total":
            string = StringVar(self.main_frame, value=val)
            value = ctk.CTkTextbox(self.main_frame, height=20, width=80)
            value.insert("0.0", val)
            value.grid(row=row_index, column=8, padx=0, pady=8)
            value.configure(state='disable')
            properties[text] = string
            row_index += 1
            continue

        string = StringVar(self.main_frame, value=val)
        value = ctk.CTkEntry(self.main_frame, textvariable=string, width=80)
        value.grid(row=row_index, column=8, padx=0, pady=8)
        properties[text] = string
        row_index += 1
from tkinter import *
import pandas as pd
import customtkinter as ctk


def student_view(self, student):
    course = self.Course
    # Top bar
    self.main_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform="equal")

    back_button = ctk.CTkButton(self.main_frame, text='Back', command=self.show_home)
    back_button.grid(row=0, column=0, pady=10, padx=10)

    name_field = ctk.CTkLabel(self.main_frame, text='Name :', font=ctk.CTkFont(size=18, weight="bold"))
    name_field.grid(row=1, column=0, padx=20, pady=(20, 10))

    student_name = ctk.CTkTextbox(self.main_frame, height=20, width=120)
    student_name.insert("0.0", student)
    student_name.grid(row=1, column=1, padx=10, pady=8)
    student_name.configure(state='disable')

    # columns
    columns_list = ['K', 'T', 'C', 'A', 'Total', 'Percentage']
    column_index = 1
    for column in columns_list:
        field = ctk.CTkLabel(self.main_frame, text=column, font=ctk.CTkFont(size=14, weight="bold"))
        field.grid(row=2, column=column_index, padx=20, pady=(20, 10))
        column_index += 1
    # data
    row_index = 3
    assessments = course.assessments
    for assessment, data in assessments.items():
        assessment_button = ctk.CTkButton(self.main_frame, text=assessment, width=120,
                                       command=None,
                                       fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        assessment_button.grid(row=row_index, column=0, pady=10, padx=10)

        df = pd.DataFrame(data)
        row = df.loc[df['Name'] == student]

        column_index = 1
        for column in row.columns:
            if column == 'Name':
                continue
            val = row[column].values[0]

            text = StringVar(self.main_frame, value=val)
            entry = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
            entry.grid(row=row_index, column=column_index, padx=0, pady=8)
            column_index += 1

        row_index += 1

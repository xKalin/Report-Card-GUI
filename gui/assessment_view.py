from tkinter import *
from gui.backend.loader.json_loader import JSONLoader
from gui.tkinter_utils import save_data

import customtkinter as ctk


def assessment_view(self, assessment_name):
    loader = JSONLoader(self, assessment_name)
    grade_df = loader.get_assessment_df()
    prop = loader.get_assessment_properties()

    # Building df frame
    # Setting columns for [Name, K, T, C A, G, %, Total (Weight, KT, CT, CC, AA)]
    self.main_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7), weight=1, uniform="equal")
    new_data = {}
    # Title bar
    label = ctk.CTkLabel(self.main_frame, text="Assessment : ", font=ctk.CTkFont(size=14, weight="bold"))
    label.grid(row=0, column=0, padx=0, pady=5)
    title = StringVar(self.main_frame, value=assessment_name)
    new_data["Assessment"] = title
    entry = ctk.CTkEntry(self.main_frame, textvariable=title, width=240)
    entry.grid(row=0, column=1, padx=0, pady=5)

    save_button = ctk.CTkButton(self.main_frame, text='Save',
                                command=(lambda frame=self:
                                         save_data(frame, assessment_name, new_data)))

    save_button.grid(row=0, column=8, padx=10, pady=10)

    # Body
    records = []
    new_data['df'] = records
    column = 0
    for column_name in grade_df.columns:
        label = ctk.CTkLabel(self.main_frame, text=column_name, font=ctk.CTkFont(size=12, weight="bold"))
        label.grid(row=1, column=column, padx=20, pady=(20, 10))
        column += 1
    grade_df.sort_values(by='Name', key=lambda x: x.apply(lambda y: y.split()[-1]), inplace=True)
    row = 2
    for index, data in grade_df.iterrows():
        row_data = {}

        student_name = ctk.CTkTextbox(self.main_frame, height=20, width=120)
        student_name.insert("0.0", data['Name'])
        student_name.grid(row=row, column=0, padx=10, pady=8)
        student_name.configure(state='disable')
        row_data['Name'] = data['Name']

        text = StringVar(self.main_frame, value=data['Knowledge'])
        knowledge = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
        knowledge.grid(row=row, column=1, padx=0, pady=8)
        row_data['Knowledge'] = text

        text = StringVar(self.main_frame, value=data['Thinking'])
        thinking = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
        thinking.grid(row=row, column=2, padx=0, pady=8)
        row_data['Thinking'] = text

        text = StringVar(self.main_frame, value=data['Communication'])
        communication = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
        communication.grid(row=row, column=3, padx=0, pady=8)
        row_data['Communication'] = text

        text = StringVar(self.main_frame, value=data['Application'])
        application = ctk.CTkEntry(self.main_frame, textvariable=text, width=80)
        application.grid(row=row, column=4, padx=0, pady=8)
        row_data['Application'] = text

        grade = ctk.CTkTextbox(self.main_frame, height=20, width=80)
        grade.insert("0.0", data['Grade'])
        grade.grid(row=row, column=5, padx=0, pady=8)
        grade.configure(state='disable')
        row_data['Grade'] = data['Grade']

        percentage = ctk.CTkTextbox(self.main_frame, height=20, width=80)
        percentage.insert("0.0", data['%'])
        percentage.grid(row=row, column=6, padx=0, pady=8)
        percentage.configure(state='disable')
        row_data['%'] = data['%']

        records.append(row_data)
        row += 1

    row_index = 2
    properties = {}
    new_data["properties"] = properties
    for text, val in prop.items():
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




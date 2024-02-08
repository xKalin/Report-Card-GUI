from tkinter import *
import customtkinter as ctk
from tkinter import filedialog
import shutil
import settings
from backend.loader.excel_loader import ExcelLoader

MEDIA = settings.MEDIA_PATH

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def refresh_assessments():
    return ExcelLoader().load_assessments()


class GradingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Loaded data
        self.assessments = refresh_assessments()

        # configure window
        self.title("Evi's Grading App")
        self.geometry(f"{1480}x{720}")

        # configure grid layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.rowconfigure(4, weight=0)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Menu", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.home_button = ctk.CTkButton(self.sidebar_frame, text='Home', command=self.show_home)
        self.home_button.grid(row=1, column=0, padx=20, pady=5)

        self.new_assignment_button = ctk.CTkButton(self.sidebar_frame, text='New Assessment',
                                                   command=self.new_assessment)
        self.new_assignment_button.grid(row=2, column=0, padx=20, pady=5)

        self.assessments_scrollbar = ctk.CTkScrollableFrame(self.sidebar_frame, height=350, label_text="Assessments")
        self.assessments_scrollbar.grid(row=3, column=0, padx=20, pady=5)
        self.assessments_to_scrollbar()

        self.delete_assessment_button = ctk.CTkButton(self.sidebar_frame, text='Delete Assessment',
                                                      command=self.delete_assessment)
        self.delete_assessment_button.grid(row=4, column=0, padx=20, pady=5)

        self.submit_button = ctk.CTkButton(self.sidebar_frame, text='Excel File(s)', command=self.load_file)
        self.submit_button.grid(row=5, column=0, padx=20, pady=5)

        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky="nsew")

        # Default view
        self.show_home()

    def show_home(self):
        self.reset_main_frame()

    @staticmethod
    def load_file():
        filepaths = filedialog.askopenfilenames(initialdir=MEDIA)
        for file in filepaths:
            shutil.copy(file, MEDIA)

    def new_assessment(self):
        pass

    def delete_assessment(self):
        pass

    def assessments_to_scrollbar(self):
        i = 0
        for assessment in self.assessments:
            assessment_button = ctk.CTkButton(master=self.assessments_scrollbar, text=assessment,
                                              command=lambda x=assessment: self.load_assessment_onto_frame(x),
                                              fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            assessment_button.grid(row=i, padx=10, pady=(0, 5))
            i += 1

    def reset_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def load_assessment_onto_frame(self, name):
        self.reset_main_frame()
        df = self.assessments[name]
        # Building df frame
        # Setting columns for [Name, K, T, C A, (Weight, KT, CT, CC, AA)]
        self.main_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1, uniform="equal")
        # Title
        label = ctk.CTkLabel(self.main_frame, text="Assessment : ", font=ctk.CTkFont(size=16, weight="bold"))
        label.grid(row=0, column=0, padx=0, pady=5)
        entry = ctk.CTkEntry(self.main_frame, placeholder_text=name, width=240)
        entry.grid(row=0, column=1, padx=0, pady=5)

        column = 0
        for column_name in df.columns[:5]:
            label = ctk.CTkLabel(self.main_frame, text=column_name, font=ctk.CTkFont(size=12, weight="bold"))
            label.grid(row=1, column=column, padx=20, pady=(20, 10))
            column += 1

        row = 2
        for column in df.columns[5:]:
            label = ctk.CTkLabel(self.main_frame, text=f"{column} : ", font=ctk.CTkFont(size=12, weight="bold"))
            label.grid(row=row, column=5, padx=0, pady=5)
            entry = ctk.CTkEntry(self.main_frame, placeholder_text='4', width=80)
            entry.grid(row=row, column=6, padx=0, pady=5)
            row += 1

        df_marks = df[['Name', 'Knowledge', 'Thinking', 'Communication', 'Application']]
        df_marks_mapping = []
        for index, data in df_marks.iterrows():
            row = index+2
            df_marks_row = []
            name = ctk.CTkLabel(self.main_frame, text=data['Name'], width=120)
            name.grid(row=row, column=0, padx=0, pady=8)
            df_marks_row.append(name)

            knowledge = ctk.CTkEntry(self.main_frame, placeholder_text=data['Knowledge'], width=80)
            knowledge.grid(row=row, column=1, padx=0, pady=8)
            df_marks_row.append(knowledge)

            thinking = ctk.CTkEntry(self.main_frame, placeholder_text=data['Thinking'], width=80)
            thinking.grid(row=row, column=2, padx=0, pady=8)
            df_marks_row.append(thinking)

            communication = ctk.CTkEntry(self.main_frame, placeholder_text=data['Communication'], width=80)
            communication.grid(row=row, column=3, padx=0, pady=8)
            df_marks_row.append(communication)

            application = ctk.CTkEntry(self.main_frame, placeholder_text=data['Application'], width=80)
            application.grid(row=row, column=4, padx=0, pady=8)
            df_marks_row.append(application)
            df_marks_mapping.append(df_marks_row)


    def load_home_frame(self):
        self.reset_main_frame()



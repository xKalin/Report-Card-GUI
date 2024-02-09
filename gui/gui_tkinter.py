import customtkinter as ctk

from gui.backend.loader.excel_loader import ExcelLoader
from gui.backend.objects.students.classroom import Classroom
from gui.assessment_view import load_assessment_onto_frame
from gui.tkinter_utils import *

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
x = 1520
y = 720


class GradingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.classroom = Classroom()

        # configure window
        self.title("Evi's Grading App")
        self.geometry(f"{x}x{y}")

        # configure grid layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.sidebar()

        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, rowspan=3, sticky="nsew")

        # Default view
        self.show_home()

    def show_home(self):
        reset_main_frame(self)
        # Menu Bar

        #

    def new_assessment(self):
        pass

    def delete_assessment(self):
        pass

    def new_student(self):
        pass

    def load_home_frame(self):
        reset_main_frame(self)

    def sidebar(self):
        # create sidebar frame with widgets
        sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        sidebar_frame.rowconfigure(4, weight=0)
        logo_label = ctk.CTkLabel(sidebar_frame, text="Menu", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        home_button = ctk.CTkButton(sidebar_frame, text='Home', command=self.show_home)
        home_button.grid(row=1, column=0, padx=20, pady=5)

        new_assignment_button = ctk.CTkButton(sidebar_frame, text='New Assessment',
                                              command=self.new_assessment)
        new_assignment_button.grid(row=2, column=0, padx=20, pady=5)

        assessments_scrollbar = ctk.CTkScrollableFrame(sidebar_frame, height=350, label_text="Assessments")
        assessments_scrollbar.grid(row=3, column=0, padx=20, pady=5)
        i = 0
        assessments = ExcelLoader().load_names()
        for assessment in assessments:
            assessment_button = ctk.CTkButton(master=assessments_scrollbar, text=assessment,
                                              command=lambda x=assessment: load_assessment_onto_frame(self, x),
                                              fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            assessment_button.grid(row=i, padx=10, pady=(0, 5))
            i += 1

        delete_assessment_button = ctk.CTkButton(sidebar_frame, text='Delete Assessment',
                                                 command=self.delete_assessment)
        delete_assessment_button.grid(row=4, column=0, padx=20, pady=5)

        submit_button = ctk.CTkButton(sidebar_frame, text='Excel File(s)', command=load_file)
        submit_button.grid(row=5, column=0, padx=20, pady=5)



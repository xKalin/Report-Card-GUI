from gui.assessment_view import assessment_view
from gui.backend.objects.course import Course
from gui.home_view import home_view
from gui.new_assessment_view import new_assessment_view
from gui.popup import course_view_popup
from gui.tkinter_utils import *

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
x = 1520
y = 720


class GradingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Grading App")
        self.geometry(f"{x}x{y}")

        # configure grid layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1), weight=1)

        # Course
        self.Course = Course()

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.rowconfigure(4, weight=0)
        self.assessments_scrollbar = None
        self.sidebar_init()

        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)

        # Default view
        #self.show_home()

    def show_home(self):
        reset_main_frame(self)
        self.main_frame.grid_forget()
        home_view(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky="nsew")

    def load_new_assessment_view(self, name):
        reset_main_frame(self)
        self.main_frame.grid_forget()
        new_assessment_view(self, name)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky="nsew")

    def load_assessment_onto_frame(self, name):
        reset_main_frame(self)
        self.main_frame.grid_forget()
        assessment_view(self, name)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky="nsew")

    def new_student(self):
        pass

    def sidebar_init(self):
        # create sidebar frame with widgets

        logo_label = ctk.CTkLabel(self.sidebar_frame, text="Grading App", font=ctk.CTkFont(size=30, weight="bold"))
        logo_label.grid(row=0, column=0, pady=(20, 10))
        home_button = ctk.CTkButton(self.sidebar_frame, text='Home', command=self.show_home)
        home_button.grid(row=1, column=0, pady=8)

        course_select = ctk.CTkButton(self.sidebar_frame, text='Course',
                                      command=lambda app=self: course_view_popup(app))
        course_select.grid(row=2, column=0, pady=8)
        self.load_assessment_scrollbar()

        excel_button = ctk.CTkButton(self.sidebar_frame, text='Excel File(s)', command=lambda val=self: load_file(val))
        excel_button.grid(row=6, column=0, pady=8)

    def load_assessment_scrollbar(self):
        selected_course = self.Course.subject

        if self.assessments_scrollbar is not None:
            self.assessments_scrollbar.destroy()
        self.assessments_scrollbar = ctk.CTkScrollableFrame(self.sidebar_frame, height=350, label_text=selected_course)
        self.assessments_scrollbar.grid(row=3, column=0, padx=20, pady=5)

        assessments = self.Course.Assessment_list
        i = 0
        for assessment in assessments:
            assessment_button = ctk.CTkButton(master=self.assessments_scrollbar, text=assessment,
                                              command=lambda var=assessment: self.load_assessment_onto_frame(var),
                                              fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            assessment_button.pack(pady=5)
            i += 1

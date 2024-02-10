from tkinter import StringVar

from gui.assessment_view import assessment_view
from gui.home_view import home_view
from gui.new_assessment_view import new_assessment_view
from gui.tkinter_utils import *

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
x = 1520
y = 720


class GradingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Evi's Grading App")
        self.geometry(f"{x}x{y}")

        # configure grid layout
        self.columnconfigure(1, weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.rowconfigure(4, weight=0)
        self.assessments_scrollbar = None
        self.sidebar_init()

        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, rowspan=3, sticky="nsew")
        # Default view
        self.show_home()

    def show_home(self):
        reset_main_frame(self)
        self.main_frame.grid_forget()
        home_view(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky="nsew")

        #

    def load_assessment_onto_frame(self, name):
        reset_main_frame(self)
        self.main_frame.grid_forget()
        assessment_view(self, name)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky="nsew")

    def new_assessment_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.attributes('-topmost', 'true')
        popup.geometry(f"{500}x{250}")
        self.eval(f'tk::PlaceWindow {str(popup)} center')
        popup.title("New Assessment")

        def close():
            popup.destroy()
            popup.update()

        def open_new_assessment_view(val):
            close()
            name = val.get()
            if validate_new_assessment(name):
                reset_main_frame(self)
                self.main_frame.grid_forget()
                new_assessment_view(self, name)
                self.main_frame.grid(row=0, column=1, padx=20, pady=20, rowspan=4, sticky="nsew")
            else:
                self.new_assessment_popup()

        ctk.CTkLabel(popup, text="New Assessment Name?",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)
        text = StringVar(popup, value="")
        ctk.CTkEntry(popup, textvariable=text, width=180).pack(pady=15)
        ctk.CTkButton(popup, text='Submit', command=lambda val=text: open_new_assessment_view(val)).pack()
        ctk.CTkButton(popup, text='Cancel', command=close).pack(pady=15)

    def delete_assessment(self):
        pass

    def new_student(self):
        pass

    def load_home_frame(self):
        reset_main_frame(self)

    def sidebar_init(self):
        # create sidebar frame with widgets

        logo_label = ctk.CTkLabel(self.sidebar_frame, text="Menu", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        home_button = ctk.CTkButton(self.sidebar_frame, text='Home', command=self.show_home)
        home_button.grid(row=1, column=0, padx=20, pady=5)

        new_assignment_button = ctk.CTkButton(self.sidebar_frame, text='New Assessment',
                                              command=self.new_assessment_popup)
        new_assignment_button.grid(row=2, column=0, padx=20, pady=5)

        self.load_assessment_scrollbar()

        delete_assessment_button = ctk.CTkButton(self.sidebar_frame, text='Delete Assessment',
                                                 command=self.delete_assessment)
        delete_assessment_button.grid(row=4, column=0, padx=20, pady=5)

        submit_button = ctk.CTkButton(self.sidebar_frame, text='Excel File(s)', command=load_file)
        submit_button.grid(row=5, column=0, padx=20, pady=5)

    def load_assessment_scrollbar(self):
        if self.assessments_scrollbar is not None:
            self.assessments_scrollbar.destroy()
        self.assessments_scrollbar = ctk.CTkScrollableFrame(self.sidebar_frame, height=350, label_text="Assessments")
        self.assessments_scrollbar.grid(row=3, column=0, padx=20, pady=5)
        i = 0
        assessments = Assessments().get_assessment_names()
        for assessment in assessments:
            assessment_button = ctk.CTkButton(master=self.assessments_scrollbar, text=assessment,
                                              command=lambda x=assessment: self.load_assessment_onto_frame(x),
                                              fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
            assessment_button.grid(row=i, padx=10, pady=(0, 5))
            i += 1

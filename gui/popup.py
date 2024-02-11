from tkinter import StringVar

import customtkinter as ctk
from CTkListbox import CTkListbox

from gui.backend.objects.assessments import Assessments
from gui.tkinter_utils import validate_new_assessment


def close(popup):
    popup.destroy()
    popup.update()


def new_assessment_popup(self):
    popup = ctk.CTkToplevel(self)
    popup.attributes('-topmost', 'true')
    popup.geometry(f"{500}x{250}")
    self.eval(f'tk::PlaceWindow {str(popup)} center')
    popup.title("New Assessment")

    def open_new_assessment_view(val):
        close(popup)
        name = val.get()
        if validate_new_assessment(name):
            self.load_new_assessment_view(name)
        else:
            new_assessment_popup(self)

    ctk.CTkLabel(popup, text="New Assessment Name?",
                 font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)
    text = StringVar(popup, value="")
    ctk.CTkEntry(popup, textvariable=text, width=180).pack(pady=15)
    ctk.CTkButton(popup, text='Submit', command=lambda val=text: open_new_assessment_view(val)).pack()
    ctk.CTkButton(popup, text='Cancel', command=lambda frame=popup: close(popup)).pack(pady=15)


def delete_assessment_popup(self):
    popup = ctk.CTkToplevel(self)
    popup.attributes('-topmost', 'true')
    popup.geometry(f"{350}x{375}")
    self.eval(f'tk::PlaceWindow {str(popup)} center')
    popup.title("Delete Assessment")

    def delete_selected_assessments():
        close(popup)
        for name in listbox.get():
            Assessments().delete_assessment(name)
        self.show_home()
        self.load_assessment_scrollbar()

    listbox = CTkListbox(popup, multiple_selection=True)
    assessments = Assessments().get_assessment_names()
    for index, assessment in enumerate(assessments):
        listbox.insert(index, assessment)
    listbox.pack(pady=25)
    ctk.CTkButton(popup, text='Delete', command=delete_selected_assessments).pack()
    ctk.CTkButton(popup, text='Cancel', command=lambda frame=popup: close(popup)).pack(pady=15)

def init_course_popup(self):
    print('course popup')
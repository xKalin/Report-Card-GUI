from tkinter import *

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
    popup.resizable(False, False)
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
    popup.resizable(False, False)
    self.eval(f'tk::PlaceWindow {str(popup)} center')
    popup.title("Delete Assessment")

    def delete_selected_assessments():
        close(popup)
        for name in listbox.get():
            Assessments().delete_assessment(name)
        self.show_home()
        self.load_assessment_scrollbar()

    listbox = CTkListbox(popup, multiple_selection=True)
    assessments = self.Course.Assessments.get_assessment_names()
    for index, assessment in enumerate(assessments):
        listbox.insert(index, assessment)
    listbox.pack(pady=25)
    ctk.CTkButton(popup, text='Delete', command=delete_selected_assessments).pack()
    ctk.CTkButton(popup, text='Cancel', command=lambda frame=popup: close(popup)).pack(pady=15)


def course_view_popup(self):
    popup = ctk.CTkToplevel(self)
    popup.attributes('-topmost', 'true')

    popup.geometry(f"{430}x{300}")
    popup.resizable(False, False)
    bg_colour = (popup.cget("bg"))
    self.eval(f'tk::PlaceWindow {str(popup)} center')
    popup.title("Courses")

    courses_box = CTkListbox(popup, label_text='Courses')
    courses = self.Course.Assessment.assessments_json
    for index, assessment in enumerate(courses):
        courses_box.insert(index, assessment)
    courses_box.pack(pady=25, padx=10, side=LEFT, anchor=NE)

    right_frame = ctk.CTkFrame(popup)
    right_frame.configure(fg_color=bg_colour)
    right_frame.pack(side=RIGHT, anchor=NW)

    def select(app):
        selected = courses_box.get()
        if selected is None:
            return
        self.Course.select_subject(selected)
        self.show_home()

    ctk.CTkButton(right_frame, text='Select', command=lambda app=self: select(app)).pack(pady=(70, 0), padx=20)

    def delete(app):
        selected = courses_box.get()
        if selected is None:
            return
        self.Course.delete_course(selected)
        if self.Course.subject == selected:
            self.Course.subject = self.Course.get_default_subject()
        courses_box.delete(courses_box.curselection())

    ctk.CTkButton(right_frame, text='Delete', command=lambda app=self: delete(app)).pack(pady=20, padx=20)

    def new(app):
        new_course_popup(app, parent=popup)

    ctk.CTkButton(right_frame, text='New', command=lambda app=self: new(app)).pack(padx=20)


def new_course_popup(self, parent):
    popup = ctk.CTkToplevel(self)
    popup.attributes('-topmost', 'true')
    popup.geometry(f"{500}x{250}+{300}+{450}")
    popup.resizable(False, False)
    popup.lift()
    popup.title("New Course")

    def new_subject(name, strVar):
        subject = name.get()
        subjects = list(self.Course.Assessment.assessments_json.keys())
        if subject == '':
            strVar.set('New Subject cannot be Blank')
            return
        if subject in subjects:
            strVar.set('New Subject already exist')
            return
        self.Course.new_course(subject)
        close(popup)
        close(parent)
        self.show_home()

    ctk.CTkLabel(popup, text="New Subject Name?",
                 font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)
    text = StringVar(popup, value="")
    ctk.CTkEntry(popup, textvariable=text, width=180).pack(pady=15)

    error_txt = StringVar(popup, value='')
    ctk.CTkLabel(popup, textvariable=error_txt).pack()

    ctk.CTkButton(popup, text='Submit', command=lambda val=text: new_subject(val, error_txt)).pack()
    ctk.CTkButton(popup, text='Cancel', command=lambda frame=popup: close(popup)).pack(pady=15)

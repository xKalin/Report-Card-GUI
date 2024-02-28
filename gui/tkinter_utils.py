import ctypes
import math
import shutil
from tkinter import filedialog, messagebox

import customtkinter as ctk
import pandas as pd

from gui.backend.calculator.assessment_calculator import AssessmentCalculator
from gui.backend.ingestor.ingest_excel import IngestExcel
from gui.backend.objects.downloader import Downloader
from settings import INGESTION_PATH, SHEETS_PATH, ASSESSMENTS_JSON_PROPERTIES_PATH, KTCA

excel_path = SHEETS_PATH
json_assessment_path = ASSESSMENTS_JSON_PROPERTIES_PATH


def previous_button(self, page):
    if page == 0:
        return
    return self.show_home(page - 1)


def next_button(self, page, length):
    per_page = 5
    max_page = math.ceil(length / per_page) - 1
    if page < max_page:
        return self.show_home(page + 1)
    return


def download_button(self):
    data = self.Course.get_students()
    df = pd.DataFrame(index=data.keys())
    for student, grades in data.items():
        df.loc[student, 'Final Grade'] = grades['Final Grade']
        for assessment, grade in grades['Assessments'].items():
            df.loc[student, assessment] = grade['Grade']
    downloader = Downloader()
    folder_selected = filedialog.askdirectory(initialdir=downloader.dst)
    if folder_selected == '':
        return
    downloader.save(folder_selected)
    download_path = f"{folder_selected}/{self.Course.subject}.xlsx"
    df.to_excel(download_path)


def load_file(self):
    filepaths = filedialog.askopenfilenames()
    if len(filepaths) == 0:
        return
    for file in filepaths:
        try:
            new_file = file.split('/')[-1]
            if new_file.split('.')[-1] != 'xlsx':
                ctypes.windll.user32.MessageBoxW(0, "Must be excel file.", "Error!", 1)
                return
            shutil.copy(file, INGESTION_PATH + new_file)
        except shutil.SameFileError:
            ctypes.windll.user32.MessageBoxW(0, "Change the name of file.", "Error!", 1)
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"{str(e)}: Report to Allen!", "Error!", 1)

    IngestExcel(self).ingest()
    self.show_home()
    self.load_assessment_scrollbar()


def reset_main_frame(self):
    for widget in self.main_frame.winfo_children():
        widget.destroy()


# SAVING LOGIC
def update_assessment(old_name, new_name, data, assessment):
    assessment_data = assessment.assessments
    if old_name != new_name:
        assessment_data[new_name] = assessment_data[old_name]
        del assessment_data[old_name]
    df = pd.DataFrame.from_records(data)
    return df.applymap(str_get)


def update_property(old_name, new_name, data, assessment):
    property_data = assessment.assessments_property
    if old_name != new_name:
        property_data[new_name] = property_data[old_name]
        del property_data[old_name]
    return get_json_from_new_data(data)


def save_data(frame, old_name, new_data):
    # popup
    popup = ctk.CTkToplevel(frame)
    popup.attributes('-topmost', 'true')
    popup.geometry(f"{500}x{250}")
    frame.eval(f'tk::PlaceWindow {str(popup)} center')
    popup.title("Save")

    def save():
        new_name = new_data['Assessment'].get()
        # Assessment.course.json
        assessment = frame.Course.Assessment

        df = update_assessment(old_name, new_name, new_data['df'], assessment)
        properties = update_property(old_name, new_name, new_data['properties'], assessment)
        df, properties = AssessmentCalculator(new_name, properties).calculate(df)
        assessment.validate_assessment_from_data_dict({'title': new_name, 'df': df, 'properties': properties})
        popup.destroy()
        popup.update()
        frame.load_assessment_scrollbar()
        if old_name != new_name:
            frame.load_assessment_scrollbar()
        frame.load_assessment_onto_frame(new_name)

    ctk.CTkLabel(popup, text="Do you wish to save?",
                 font=ctk.CTkFont(size=30, weight="bold")).pack(pady=30)
    ctk.CTkButton(popup, text='Save', command=save).pack()

    def close():
        popup.destroy()
        popup.update()

    ctk.CTkButton(popup, text='Cancel', command=close).pack(pady=15)


def get_df_from_new_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.applymap(str_get)
    return df


def get_json_from_new_data(json_dict):
    ktca_list = KTCA
    new_total = 0
    for ktcaw in json_dict:
        value = json_dict[ktcaw].get()
        json_dict[ktcaw] = value
        if ktcaw in ktca_list:
            new_total += float(value)
    json_dict['Total'] = new_total
    return json_dict


def str_get(cell):
    try:
        return cell.get()
    except Exception as e:
        return cell


def validate_new_assessment(self, new_name):
    names = self.Course.Assessment.get_assessment_names()
    if new_name == "":
        messagebox.showwarning('Python Error', 'Assessment Cannot be Blank')
        return False
    if names:
        if new_name in names:
            messagebox.showwarning('Python Error', 'Assessment Cannot be Blank')
            return False
    return True


def validate_new_student(self, new_student):
    names = self.Course.get_students()
    if new_student == "":
        messagebox.showwarning('Python Error', 'Student Cannot be Blank')
        return False
    if len(new_student.split()) < 2:
        messagebox.showwarning('Python Error', 'Student has no last name')
        return False
    if names:
        if new_student in names:
            messagebox.showwarning('Python Error', 'Student Already Exists')
            return False
    return True

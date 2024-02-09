import json
import os
import shutil
from tkinter import filedialog

import customtkinter as ctk
import pandas as pd

from settings import MEDIA_PATH, SHEETS_PATH, ASSESSMENTS_PATH

excel_path = SHEETS_PATH
json_assessment_path = ASSESSMENTS_PATH


def load_file():
    filepaths = filedialog.askopenfilenames(initialdir=MEDIA_PATH)
    for file in filepaths:
        shutil.copy(file, MEDIA_PATH)


def reset_main_frame(self):
    for widget in self.main_frame.winfo_children():
        widget.destroy()


# SAVING LOGIC
def save_data(frame, old_data, new_data):
    # popup
    popup = ctk.CTkToplevel(frame)
    popup.attributes('-topmost', 'true')
    popup.geometry(f"{500}x{250}")
    frame.eval(f'tk::PlaceWindow {str(popup)} center')
    popup.title("Save")

    def save():
        def rename_assessment(old_name, new_name):
            if old_name == new_name:
                return old_name
            old_filepath = f"{excel_path}/{old_name}.xlsx"
            new_filepath = f"{excel_path}/{new_name}.xlsx"
            os.rename(old_filepath, new_filepath)
            refresh_json_assessment(old_name, new_name, new_data['json'])

        assessment = rename_assessment(old_data['Assessment'], new_data['Assessment'].get())
        new_df = get_df_from_new_data(new_data['df'])
        old_df = old_data['df']
        if not old_df.equals(new_df):
            new_df.to_excel(f"{excel_path}/{assessment}.xlsx", index=False)

        popup.destroy()
        popup.update()
        # return home update sidebar

    ctk.CTkLabel(popup, text="Do you wish to save?",
                 font=ctk.CTkFont(size=30, weight="bold")).pack(pady=30)
    ctk.CTkButton(popup, text='Save', command=save).pack()

    def close():
        popup.destroy()
        popup.update()

    ctk.CTkButton(popup, text='Cancel', command=close).pack(pady=15)


def refresh_json_assessment(old_name, new_name, new_data):
    json_data = get_json_from_new_data(new_data['json'])
    with open(json_assessment_path) as f:
        data = json.load(f)
    data[old_name] = data[new_name]
    del data[old_name]
    data[new_name] = json_data
    with open(json_assessment_path, "w") as f:
        json.dump(data, fp=f, ensure_ascii=False, indent=4)


def get_df_from_new_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.applymap(str_get)
    return df


def get_json_from_new_data(json_dict):
    for ktca in json_dict:
        json_dict[ktca] = json_dict[ktca].get()
    return json_dict


def str_get(cell):
    try:
        return cell.get()
    except Exception as e:
        return cell

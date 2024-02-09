import os

import pandas as pd

import settings


class ExcelLoader:

    def __init__(self):
        self.sheets_path = settings.SHEETS_PATH

    def load(self, assessment_name):
        return pd.read_excel(f'{self.sheets_path}/{assessment_name}.xlsx')

    def load_all(self):
        assessments = {}
        for file in os.listdir(self.sheets_path):
            assessment_name = file.replace('.xlsx', '')
            assessments[assessment_name] = (pd.read_excel(f'{self.sheets_path}/{file}'))
        return assessments

    def load_names(self):
        assessments = {}
        for file in os.listdir(self.sheets_path):
            assessment_name = file.replace('.xlsx', '')
            assessments[assessment_name] = assessment_name
        return assessments



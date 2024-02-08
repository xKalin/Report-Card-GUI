import os

import pandas as pd

import settings


class ExcelLoader:

    def __init__(self):
        self.sheets_path = settings.SHEETS_PATH

    def load_assessments(self):
        assessments = {}
        for file in os.listdir(self.sheets_path):
            assessment_name = file.replace('.xlsx', '')
            assessments[assessment_name] = (pd.read_excel(f'{self.sheets_path}/{file}'))
        return assessments

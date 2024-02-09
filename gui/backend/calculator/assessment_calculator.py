import json

import pandas as pd

from settings import ASSESSMENTS_PROPERTIES_PATH


class AssessmentCalculator:
    def __init__(self, name):
        self.name = name
        self._properties = self.get_properties()
        self.total = self.get_total()

    def calculate(self, df):
        df['Grade'] = df.apply(self.add_rows, axis=1)
        df['%'] = df['Grade'].apply(self.get_average)
        return df, self._properties[self.name]

    @staticmethod
    def get_properties():
        path = ASSESSMENTS_PROPERTIES_PATH
        with open(path) as f:
            data = json.load(f)
        return data

    def set_properties(self, prop):
        self._properties[self.name] = prop
        return self._properties

    def get_total(self):
        assessment = self._properties[self.name]
        total = float(assessment['Knowledge']) if assessment['Knowledge'] is not None else 0
        total += float(assessment['Thinking']) if assessment['Thinking'] is not None else 0
        total += float(assessment['Communication']) if assessment['Communication'] is not None else 0
        total += float(assessment['Application']) if assessment["Application"] is not None else 0
        return total

    @staticmethod
    def add_rows(row):
        grade = float(row['Knowledge']) if row['Knowledge'] is not None else 0
        grade += float(row['Thinking']) if row['Thinking'] is not None else 0
        grade += float(row['Communication']) if row['Communication'] is not None else 0
        grade += float(row['Application']) if row["Application"] is not None else 0
        return grade

    def get_average(self, grade):
        average = str(float(grade)/self.total * 100)
        if average == 'nan':
            return ''
        return average + '%'

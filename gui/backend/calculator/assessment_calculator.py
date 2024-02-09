import json

import pandas as pd

from settings import ASSESSMENTS_PATH


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
        path = ASSESSMENTS_PATH
        with open(path) as f:
            data = json.load(f)
        return data

    def set_properties(self, prop):
        self._properties[self.name] = prop
        return self._properties

    def get_total(self):
        assessment = self._properties[self.name]
        total = 0
        total += assessment['Knowledge']
        total += assessment['Thinking']
        total += assessment['Communication']
        total += assessment['Application']
        return total

    @staticmethod
    def add_rows(row):
        grade = row['Knowledge']
        grade += row['Thinking']
        grade += row['Communication']
        grade += row['Application']
        return grade

    def get_average(self, grade):
        average = str(float(grade/self.total) * 100)
        if average == 'nan':
            return ''
        return average + '%'

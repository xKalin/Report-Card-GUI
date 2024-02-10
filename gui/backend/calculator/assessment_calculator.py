import json
import math

import pandas as pd

from settings import ASSESSMENTS_PROPERTIES_PATH, KTCA


class AssessmentCalculator:
    def __init__(self, name, properties=None):
        self.name = name
        self._properties = properties if properties else self.get_properties()
        self.total = self.get_total()

    def calculate(self, df):
        df['Grade'] = df.apply(self.add_rows, axis=1)
        df['%'] = df['Grade'].apply(self.get_average)
        return df, self._properties

    def get_properties(self):
        path = ASSESSMENTS_PROPERTIES_PATH
        with open(path) as f:
            data = json.load(f)
        return data[self.name]

    def get_total(self):
        assessment = self._properties
        total = 0
        for ktca in KTCA:
            total += float(assessment[ktca]) if assessment[ktca] is not None else 0
        return total

    @staticmethod
    def add_rows(row):
        grade = 0
        for ktca in KTCA:
            try:
                if math.isnan(float(row[ktca])):
                    continue
                grade += float(row[ktca])
            except Exception as e:
                grade += 0
        return grade

    def get_average(self, grade):
        if grade == 'N/A':
            return 'N/A'
        average = str(float(grade)/self.total * 100)
        if average == 'nan':
            return ''
        return average + '%'

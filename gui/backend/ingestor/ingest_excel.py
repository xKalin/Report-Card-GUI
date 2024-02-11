import os
import pandas as pd

from settings import INGESTION_PATH


class IngestExcel:
    def __init__(self, app):
        self.path = INGESTION_PATH
        self.app = app

    def ingest(self):
        filenames = next(os.walk(self.path), (None, None, []))[2]  # [] if no file
        course = self.app.Course
        assessment = course.Assessment
        for file in filenames:
            df = pd.read_excel(f'{self.path}/{file}')
            title = file.replace('.xlsx', '')
            course.validate_students_from_excel(df)
            assessment.validate_assessment_from_excel({"title": title, "df": df})


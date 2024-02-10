import os
import pandas as pd

from gui.backend.calculator.assessment_calculator import AssessmentCalculator
from gui.backend.objects.assessments.Assessments import Assessments
from gui.backend.objects.students.course import Course
from settings import INGESTION_PATH


class IngestExcel:
    def __init__(self):
        self.path = INGESTION_PATH

    def ingest(self):
        filenames = next(os.walk(self.path), (None, None, []))[2]  # [] if no file
        course = Course()
        assessment = Assessments()
        for file in filenames:
            df = pd.read_excel(f'{self.path}/{file}')
            title = file.replace('.xlsx', '')
            course.validate_students_from_excel(df)
            assessment.validate_assessment_from_excel({"title": title, "df": df})


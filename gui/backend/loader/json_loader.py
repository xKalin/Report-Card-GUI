import os

import pandas as pd

import settings
from gui.backend.objects.assessments.Assessments import Assessments
from gui.backend.objects.students.course import Course


class JSONLoader:

    def __init__(self, name):
        self.assessment_name = name
        self.Assessments = Assessments()
        self.Course = Course()

    def get_assessment_df(self):
        assessments = self.Assessments.assessments[self.assessment_name]
        df = pd.DataFrame.from_records(assessments)
        return df

    def get_assessment_properties(self):
        return self.Assessments.assessments_property[self.assessment_name]
    def get_classroom_df(self):
        pass



import pandas as pd


class JSONLoader:

    def __init__(self, app, name):
        self.app = app
        self.assessment_name = name
        self.Course = app.Course
        self.Assessments = self.Course.Assessment

    def get_assessment_df(self):
        assessments = self.Assessments.assessments[self.assessment_name]
        df = pd.DataFrame.from_records(assessments)
        return df

    def get_assessment_properties(self):
        return self.Assessments.assessments_property[self.assessment_name]

    def get_classroom_df(self):
        pass

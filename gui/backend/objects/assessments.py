import json

from gui.backend.calculator.assessment_calculator import AssessmentCalculator
from settings import ASSESSMENTS_JSON_PATH, ASSESSMENTS_JSON_PROPERTIES_PATH


class Assessments:
    def __init__(self, subject):
        self._assessment_path = ASSESSMENTS_JSON_PATH
        self._prop_path = ASSESSMENTS_JSON_PROPERTIES_PATH
        self.subject = subject
        self.assessments, self.assessments_property = self._from_json()

    def delete_assessment(self, assessment_name):
        del self.assessments[assessment_name]
        del self.assessments_property[assessment_name]
        self.save_assessments_json()

    def validate_assessment_from_excel(self, data):
        title = data['title']
        self.assessments_property[title] = self.get_default_properties()
        df, properties = AssessmentCalculator(data['title'], self.assessments_property[title]).calculate(data['df'])
        records = json.loads(df.to_json(orient="records"))
        self.assessments[title] = records
        self.save_assessments_json()

    def validate_assessment_from_data_dict(self, data):
        title = data['title']
        records = json.loads(data['df'].to_json(orient="records"))
        self.assessments[title] = records
        self.assessments_property[title] = data['properties']
        self.save_assessments_json()

    def save_assessments_json(self):
        with open(self._assessment_path, "w") as f:
            json.dump(self.assessments, fp=f, ensure_ascii=False, indent=4)
        with open(self._prop_path, "w") as f:
            json.dump(self.assessments_property, fp=f, ensure_ascii=False, indent=4)

    def get_assessment_names(self):
        return self.assessments.keys()

    def _from_json(self):
        with open(self._assessment_path) as f:
            assessments = json.load(f)
        with open(self._prop_path) as f:
            properties = json.load(f)
        return assessments[self.subject], properties[self.subject]

    @staticmethod
    def get_assessment_columns():
        return ["Names", "Knowledge", "Thinking", "Communication", "Application", "Grade", "%"]

    @staticmethod
    def get_default_properties():
        return {
            "Knowledge": "4",
            "Thinking": "4",
            "Communication": "4",
            "Application": "4",
            "Total": "16",
            "Weight": "None"
        }
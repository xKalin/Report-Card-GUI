class FinalGradeCalculator:
    def __init__(self, assessment, properties):
        self.Assessments = assessment
        self.Properties = properties

    def calculate(self, student_name):
        weight = self.weight_validation()
        final_grade = 0
        assessments = {}
        for assessment, data_list in self.Assessments.items():
            data = next(classroom for classroom in data_list if classroom["Name"] == student_name)
            current_assessment_grade = float(data['%'].replace('%', ''))
            final_grade += current_assessment_grade

            assessments[assessment] = {
                "Grade": current_assessment_grade,
                "Weight": weight[assessment] if weight != "EQUAL" else "EQUAL"
            }
        final_grade = "{:.2f}".format(final_grade / len(self.Assessments)) + '%'
        return final_grade, assessments

    def weight_validation(self):
        # TODO : Weight validation is EQUAL
        # OtherWise Return Weight validation as list of Assessments: weight%
        return 'EQUAL'

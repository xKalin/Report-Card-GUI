class Students:
    def __init__(self, name, grade, comment, assessments=[]):
        self.name = name
        self.grade = grade
        self.comment = comment
        self.assessments = assessments

    def serialize_student(self):
        return {
            self.name: {
                "grade": self.grade,
                "comment": self.comment,
                "assessments": self.assessments
            }
        }

    def add_assessment(self, assessment):
        self.assessments.append(assessment)


"""
[
   {
      "name":"example_student",
      "grade":0,
      "comments"0,
      "assessments":[
         {
            "name":"Test1",
            "knowledge":"1/4",
            "thinking":"1/4",
            "communication":"1/4",
            "application":"1/4",
            "mark":"0.25",
            "weight":"None"
         }
      ]
   }
]

"""

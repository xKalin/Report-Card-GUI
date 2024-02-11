class Students:

    def add_students(self, student_dict, df):
        for index, row in df.iterrows():
            student_dict[row['Name']] = {}

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

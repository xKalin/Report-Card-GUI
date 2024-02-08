from abc import ABC, abstractmethod


class Student:

    def __init__(self, name):
        self.name = name
        self.grade = 0
        self.average = 0
        self.assessments = []

    def set_name(self, name):
        self.name = name

    def student_to_json(self):
        pass

    def get_student_json(self):
        pass


"""
[
   {
      "name":"example_student",
      "grade":0,
      "average":0,
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

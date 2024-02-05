from abc import ABC, abstractmethod


class Category(ABC):

    def __init__(self, grade: int, total: int):
        self.grade = grade
        self.total = total

    def get_grade_as_percent(self):
        percent_grade = float(self.grade / self.total)
        return float("{:.2f}".format(percent_grade))


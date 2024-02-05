from abc import ABC, abstractmethod


class Student:

    def __init__(self, name):
        self.name = name
        self.grades = []

    def set_name(self, name):
        self.name = name

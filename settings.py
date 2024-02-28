import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


INGESTION_PATH = resource_path(r'media/ingestion/')
SHEETS_PATH = resource_path(r'media/sheets')
STUDENTS_JSON_PATH = resource_path(r'media/data/students.json')
ASSESSMENTS_JSON_PATH = resource_path(r'media/data/assessments.json')
ASSESSMENTS_JSON_PROPERTIES_PATH = resource_path(r'media/data/assessments_properties.json')
DST_PATH = resource_path(r'media/data/dst.json')
ICON = resource_path(r'media/assets/icon.ico')
KTCA = ["Knowledge", 'Thinking', 'Application', "Communication"]

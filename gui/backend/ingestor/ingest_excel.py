import os
import pandas as pd

import settings


class IngestExcel:
    @staticmethod
    def get_data():
        sheets = []
        path = settings.MEDIA_PATH
        filenames = next(os.walk(path), (None, None, []))[2]  # [] if no file
        for file in filenames:
            sheets.append(pd.read_excel(f'{path}/{file}', sheet_name=None))
        return sheets

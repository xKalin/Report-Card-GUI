class Students:

    def add_students(self, student_dict, df):
        for index, row in df.iterrows():
            student_dict[row['Name']] = {}

import pandas as pd

class Student:
    def __init__(self, roll_no, name, year, semester, courses, programme):
        self.roll_no = roll_no
        self.name = name
        self.year = year
        self.semester = semester
        self.courses = courses
        self.programme = programme

    def __str__(self):
        return f"Student({self.roll_no}, {self.name}, {self.year}, {self.semester}, {self.courses}, {self.programme})"

df = pd.read_excel('test_file.xlsx', engine='openpyxl')

course_dict = {}

for _, row in df.iterrows():

    roll_no = row['Student Roll']
    name = row['Name']
    year = row['Year']
    semester = row['Semester']
    programme = row['Programme']
    courses = row[5:15].tolist()

    courses = [course for course in courses if pd.notnull(course)]


    student = Student(roll_no, name, year, semester, courses, programme)

    for course in courses:
        if course not in course_dict:
            course_dict[course] = []
        course_dict[course].append(student)

for key in course_dict:
    print(key)
    for student in course_dict[key]:
        print(student)

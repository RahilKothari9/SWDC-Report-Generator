import pandas as pd


class Classrooms:
    def __init__(self, building, room, capacity):
        self.building = building
        self.room = room
        self.capacity = capacity

    def __str__(self):
        return f"Classrooms({self.building}, {self.room}, {self.capacity})"
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
    
class Arrangement:
    def __init__(self, from_roll_number, to_roll_number="Default", date="Default", course_code="Default", course_name="Default", semester="Default", year="default", classroom_code="default", programme="Default"):
        self.from_roll_number = from_roll_number
        self.to_roll_number = to_roll_number
        self.date = date
        self.course_code = course_code
        self.course_name = course_name
        self.semester = semester
        self.year = year
        self.classroom_code = classroom_code
        self.student_list = []
        self.programme = programme

def get_classrooms(path: str = None):
    if path is None or path == "":
        raise Exception("Path Not Provided")
    try:
        df = pd.read_excel(path, sheet_name=None, header=0, index_col=0)
        classrooms = []
        for sheet in df:
            df[sheet].index = df[sheet].index.astype(str)
            for index, row in df[sheet].iterrows():
                classrooms.append(Classrooms(sheet, index, row['Capacity']))
        sorted_classrooms = sorted(classrooms, key=lambda x: x.capacity, reverse=True)
        return classrooms
    except Exception as e:
        print(e)
        return None
    
def get_students(path: str = None):
    df = pd.read_excel(path, engine='openpyxl')
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
    sorted_courses = dict(sorted(course_dict.items(), key=lambda item: len(item[1]), reverse=True))
    return sorted_courses


classrooms = get_classrooms("Classes.xlsx")
courses = get_students("test_file.xlsx")

# for key in courses:
#     print(key)
#     for i in courses[key]:
#         print(i)

# print("Classrooms\n\n\n")
# for classes in classrooms:
#     print(classes)

def create_arrangements(courses, classrooms):
    arrangements = []
    l = 0
    r = 0
    subject_list = tuple(courses.keys())
    students_list = tuple(courses.values())
    student_pointer = 0
    while(r != len(subject_list)):
        
        current_course = students_list[r]
        
            
        
        #print(classrooms[l].capacity)
        a = Arrangement(from_roll_number=current_course[student_pointer].roll_no, classroom_code=(classrooms[l].building+classrooms[l].room), course_code=subject_list[r], semester=current_course[student_pointer].semester, year=current_course[student_pointer].year, programme=current_course[student_pointer].programme)
        while (student_pointer != len(current_course) and classrooms[l].capacity > 0):
            # print("HELLO")
            a.student_list.append(current_course[student_pointer])
            student_pointer += 1
            classrooms[l].capacity -= 1
        if(classrooms[l].capacity == 0):
            l += 1
            a.to_roll_number = current_course[student_pointer - 1].roll_no
            arrangements.append(a)
        if(student_pointer == len(current_course)):
            r += 1
            l += 1
            student_pointer = 0
            a.to_roll_number = current_course[student_pointer - 1].roll_no
            arrangements.append(a)
        if(l == len(classrooms)):
            print ("Create a third Building")
            break
    return arrangements

x = create_arrangements(courses, classrooms)

for a in x:
    print(f"{a.classroom_code}  {len(a.student_list)} {a.course_code} {a.from_roll_number} to {a.to_roll_number}")
    
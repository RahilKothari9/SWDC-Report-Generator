from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Example classrooms and capacities
classrooms = {
    'B101': 30,
    'B201': 60,
    # Add more classrooms as needed
}

# Example subjects with specified course codes
subjects = [
    {'name': 'Data Definition Language', 'course_code': 'DDL', 'semester': 1},
    {'name': 'Theory and Computation', 'course_code': 'TACD', 'semester': 1},
    {'name': 'Relational Database Management System', 'course_code': 'RDBMS', 'semester': 1},
    {'name': 'Programming Structures and Object Technology', 'course_code': 'PSOT', 'semester': 1},
    {'name': 'MERN Stack', 'course_code': 'MERN', 'semester': 1},
]

students_df = pd.DataFrame(columns=['Year', 'Programme', 'Semester', 'Student Roll', 'Name', 
                                    'Course Code 1', 'Course Code 2', 'Course Code 3', 'Course Code 4', 
                                    'Course Code 5', 'Course Code 6', 'Course Code 7', 'Course Code 8', 
                                    'Course Code 9', 'Course Code 10'])

def allocate_students_to_classrooms(students, classrooms, selected_subjects):
    allocation = {classroom: [] for classroom in classrooms}
    classroom_keys = list(classrooms.keys())
    class_index = 0

    for subject in selected_subjects:
        current_classroom = classroom_keys[class_index]
        capacity_left = classrooms[current_classroom]
        print(selected_subjects)
        print(students)
        subject_students = students[students.apply(lambda x: subject in x[['Course Code 1', 'Course Code 2', 'Course Code 3', 'Course Code 4', 'Course Code 5', 'Course Code 6', 'Course Code 7', 'Course Code 8', 'Course Code 9', 'Course Code 10']].values, axis=1)]
        print(subject_students)
        if subject_students.empty:
            continue

        for _, student in subject_students.iterrows():
            if capacity_left == 0:
                class_index += 1
                if class_index < len(classroom_keys):
                    current_classroom = classroom_keys[class_index]
                    capacity_left = classrooms[current_classroom]
                else:
                    raise Exception("Not enough classroom capacity to allocate all students")

            allocation[current_classroom].append(student)
            capacity_left -= 1

    return allocation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seating_plan', methods=['GET', 'POST'])
def seating_plan():
    if request.method == 'POST':
        selected_subjects = request.form.getlist('subjects')
        allocation = allocate_students_to_classrooms(students_df, classrooms, selected_subjects)

        seating_plan_data = []
        for classroom, students in allocation.items():
            roll_numbers = [student['Student Roll'] for student in students]
            if roll_numbers:
                seating_plan_data.append({
                    'classroom': classroom,
                    'roll_range': f"{min(roll_numbers)} - {max(roll_numbers)}"
                })

        return render_template('seating_plan.html', seating_plan=seating_plan_data)
    
    return render_template('select_subjects.html', subjects=subjects)

@app.route('/roll_call_list')
def roll_call_list():
    return render_template('roll_call_list.html', students=students_df.to_dict(orient='records'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            global students_df
            students_df = pd.read_excel(filepath)
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

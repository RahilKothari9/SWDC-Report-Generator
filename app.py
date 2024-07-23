from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = '3d6f45a5fc12445dbac2f59c3b6c7cb1'

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Example classrooms and capacities
classrooms = {
    'B101': 30,
    'B102': 35,
    'B103': 40,
    'B201': 60,
    'B202': 55,
    'B203': 50,
    'B204': 45,
    'B205':60,
    'B301': 45,
    'B401': 50,
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
    allocation = {}
    available_classrooms = list(classrooms.keys())

    for subject in selected_subjects:
        subject_students = students[students.apply(lambda x: subject in x[['Course Code 1', 'Course Code 2', 'Course Code 3', 'Course Code 4', 'Course Code 5', 'Course Code 6', 'Course Code 7', 'Course Code 8', 'Course Code 9', 'Course Code 10']].values, axis=1)]
        
        if subject_students.empty:
            continue

        total_students = len(subject_students)
        allocated_students = 0

        while allocated_students < total_students:
            if not available_classrooms:
                raise Exception(f"Not enough classrooms to allocate all students for {subject}")

            current_classroom = available_classrooms.pop(0)
            capacity = classrooms[current_classroom]

            students_to_allocate = min(capacity, total_students - allocated_students)
            allocation[current_classroom] = {
                'subject': subject,
                'students': subject_students.iloc[allocated_students:allocated_students + students_to_allocate]
            }
            allocated_students += students_to_allocate

            if allocated_students < total_students:
                # If we need more classrooms for this subject, continue to the next iteration
                continue
            elif available_classrooms:
                # If we've allocated all students for this subject and there are still classrooms available,
                # move to the next subject
                break
            else:
                # If we've used all classrooms, stop allocation
                return allocation

    return allocation

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', subjects=subjects)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and file.filename.endswith('.xlsx'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        global students_df
        students_df = pd.read_excel(filepath)
        session['file_uploaded'] = True
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/select_subjects', methods=['POST'])
def select_subjects():
    selected_subjects = request.form.getlist('subjects')
    session['selected_subjects'] = selected_subjects
    return redirect(url_for('index'))

@app.route('/seating_plan')
def seating_plan():
    if 'file_uploaded' not in session or 'selected_subjects' not in session:
        return redirect(url_for('index'))
    
    selected_subjects = session['selected_subjects']
    allocation = allocate_students_to_classrooms(students_df, classrooms, selected_subjects)

    seating_plan_data = []
    for classroom, data in allocation.items():
        students = data['students']
        roll_numbers = students['Student Roll'].tolist()
        seating_plan_data.append({
            'classroom': classroom,
            'subject': data['subject'],
            'num_students': len(students),
            'roll_range': f"{min(roll_numbers)} - {max(roll_numbers)}"
        })

    return render_template('seating_plan.html', seating_plan=seating_plan_data)

@app.route('/roll_call_list')
def roll_call_list():
    if 'file_uploaded' not in session or 'selected_subjects' not in session:
        return redirect(url_for('index'))
    
    selected_subjects = session['selected_subjects']
    allocation = allocate_students_to_classrooms(students_df, classrooms, selected_subjects)

    classroom_data = {}
    for classroom, data in allocation.items():
        subject_code = data['subject']
        subject_info = next(subject for subject in subjects if subject['course_code'] == subject_code)
        classroom_data[classroom] = {
            'subject_name': subject_info['name'],
            'subject_code': subject_code,
            'programme': 'T.Y. B.Tech Computer Engineering',  # You may need to adjust this
            'semester': subject_info['semester'],
            'students': data['students'].to_dict(orient='records')
        }

    exam_date = datetime.now().strftime("%d.%m.%Y")
    exam_time = "2.30 PM - 5.30 PM"  # You may want to make this dynamic
    exam_session = "Afternoon"  # You may want to make this dynamic

    return render_template('roll_call_list.html', 
                           classroom_data=classroom_data, 
                           exam_date=exam_date,
                           exam_time=exam_time,
                           exam_session=exam_session)

if __name__ == '__main__':
    app.run(debug=True)
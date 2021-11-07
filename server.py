"""Server for assessments app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
from jinja2 import StrictUndefined
from datetime import date
from pprint import pprint

import crud

app = Flask(__name__)
app.secret_key = 'VLF8AsFAy!qbrkdN6Ra$6F#-!UrNBT'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    
    # If there's a user logged in, show choices for next step
    if session.get("username"):
        user_id = crud.get_user_by_username(session["username"]).user_id
        # Use today's date to determine academic year
        academic_year = crud.get_academic_year_by_date(date.today())
        # Using logged in user info + academic year to get a list of
        # schools and grades that this user teaches
        schools_grades = crud.get_schools_grades_for_teacher(user_id, academic_year.academic_year_id)
        
        schools = [school.school for school in schools_grades]
        schools = list(set(schools))
        schools.sort(key=lambda school: school.name)
        
        grades = [school.grade for school in schools_grades]
        grades = list(set(grades))
        grades.sort()

        return render_template('homepage.html', schools=schools, grades=grades)

    return render_template('homepage.html')


@app.route('/login', methods=['POST'])
def process_login():
    """Process user login"""

    username = request.form.get("username")
    password = request.form.get("password")

    user = crud.get_user_by_username(username)
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        
    else:
        # Log in user by storing the user's email in session
        session["username"] = username
        flash(f"Login successful!")

    return redirect("/")


@app.route("/logout")
def process_logout():
    """Log user out"""

    session.pop("username", None)
    flash("Log out successful!")
    
    return redirect("/")


@app.route('/assessment/')
def students_by_teacher():

    # If no user is logged in, reject request
    if not session.get("username"):
        flash("Please log in first.")
        return redirect("/")

    assessment_name = request.args.get("assessment_name")
    grade = request.args.get("grade")
    school_id = request.args.get("school_id")

    username = session.get("username")
    user_id = crud.get_user_by_username(username).user_id

    academic_year_id = crud.get_academic_year_by_date(date.today()).academic_year_id

    students = crud.get_student_roster_by_teacher(user_id, school_id, grade, academic_year_id)
    students = [student.student for student in students]
    students.sort(key=lambda student: student.first_name)
    
    student_ass = [student.student_assessments for student in students]
    rosters = [student.rosters for student in students]
    teacher = crud.get_user_by_username(username)
    today = date.today().strftime("%m/%d/%y")

    return render_template(f"/assessment.html", 
                            assessment_name=assessment_name, 
                            students=students, 
                            rosters=rosters, 
                            teacher=teacher, 
                            student_ass=student_ass, 
                            today=today)


@app.route('/assessment/<assessment_name>', methods=['POST'])
def record_entries(assessment_name):
    
    teacher = {"first_name": request.form.get('teacher_first'),
                "last_name": request.form.get('teacher_last'),
                "username": request.form.get('teacher_username')}

    assessment_name = assessment_name

    # Find Assessment ID for this assessment
    assessment_id = crud.get_assessment_by_name(assessment_name).assessment_id

    # Given Assessment ID and today's date, get Scoring Term ID
    scoring_term_id = crud.get_scoring_term_by_assessment_id_and_date(assessment_id, date.today()).scoring_term_id

    # for k, v in request.form.items():
    #     entry_dict.append({k: v})
    entries = []

    student_ids = request.form.getlist('student_id')
    scores = request.form.getlist('score')
    exemption_ids = request.form.getlist('exemption_id')

    for i, sid in enumerate(student_ids):
        entries.append({'student_id': sid, 'score': scores[i], 'exemption_id': exemption_ids[i]})
    
    print(pprint(entries))
    print(f"assessment {assessment_name}")
    print(f"teacher {teacher}")
    
    return render_template('report.html', 
                            teacher=teacher,
                            assessment_name=assessment_name, 
                            entries=entries)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0", port=5001, debug=True)

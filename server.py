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

BAS_SCORES = ("subA","A","B","C","D","E","F","G","H","I",
            "J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")
BAS_LEVELS = ("Below","Meets","Exceeds")

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

        # Get assessments to display
        assessments = crud.all_assessments()
        assessments = [assessment for assessment in assessments]
        assessments.sort(key=lambda assessment: assessment.name)

        schools = [school.school for school in schools_grades]
        schools = list(set(schools))
        schools.sort(key=lambda school: school.name)
        
        grades = [school.grade for school in schools_grades]
        grades = list(set(grades))
        grades.sort()

        return render_template('homepage.html', assessments=assessments, schools=schools, grades=grades)

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

    assessment_id = request.args.get("assessment_id")
    assessment = crud.get_assessment_by_id(assessment_id)

    grade = request.args.get("grade")
    school_id = request.args.get("school_id")

    username = session.get("username")
    user = crud.get_user_by_username(username)

    academic_year = crud.get_academic_year_by_date(date.today())

    students = crud.get_student_roster_by_teacher(user.user_id, school_id, grade, academic_year.academic_year_id)
    students = [student.student for student in students]
    students.sort(key=lambda student: student.first_name)
    
    student_assessments = [student.student_assessments for student in students]
    rosters = [student.rosters for student in students]
    today = date.today().strftime("%m/%d/%y")

    return render_template(f"/assessment.html", 
                            assessment=assessment, 
                            students=students, 
                            rosters=rosters, 
                            user=user, 
                            student_assessments=student_assessments, 
                            today=today,
                            grade=grade)


@app.route('/assessment/<assessment_id>', methods=['POST'])
def record_entries(assessment_id):
    
    # Collect form data
    grade = request.form.get('grade')
    username = request.form.get('username')
    student_ids = request.form.getlist('student_id')
    first_names = request.form.getlist('first_name')
    last_names = request.form.getlist('last_name')
    scores = request.form.getlist('score')
    exemption_ids = request.form.getlist('exemption_id')

    # Get Teacher by the Username
    user = crud.get_user_by_username(username)

    # Get Assessment by its ID
    assessment = crud.get_assessment_by_id(assessment_id)

    # Get Scoring Term given Assessment ID and today's date
    scoring_term = crud.get_scoring_term_by_assessment_id_and_date(assessment_id, date.today())

    # Get benchmark by Assessment ID, Grade, Term, then get score cutoff
    benchmark = crud.get_benchmark_by_assessment_id_grade_term(assessment.assessment_id, grade, scoring_term.term)
    cutoff = benchmark.cutoff

    # Get academic year by today's date
    academic_year = crud.get_academic_year_by_date(date.today())

    # Group student data within a list and add the data into the database
    entries = []

    for i, sid in enumerate(student_ids):

        # Determine a student's level based on his/her score
        if cutoff and scores[i]:
            if scores[i] < cutoff or scores[i] == "subA":
                level = "Below"
            elif scores[i] == cutoff:
                level = "Meets"
            elif scores[i] > cutoff:
                level = "Exceeds"
            else:
                level = ""
        else:
            level = ""
        
        # Display entries and level
        entries.append({'student_id': sid, 'score': scores[i], 'first_name': first_names[i], 
                        'last_name': last_names[i], 'level': level, 'exemption_id': exemption_ids[i]})
        
        # Convert data from Form grab into int
        sid = int(sid) if sid else None
        xid = int(exemption_ids[i]) if exemption_ids[i] else None

        # Add newly entered data to database
        crud.create_student_assessment(sid, scoring_term.scoring_term_id, xid, 
                                    scores[i], benchmark.benchmark_id, date.today())

    tests = crud.all_student_assessments()
    print(tests)

    return render_template('report.html', 
                            user=user,
                            assessment=assessment, 
                            entries=entries,
                            term=scoring_term.term,
                            academic_year=academic_year.year,
                            grade=grade,
                            cutoff=cutoff)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0", port=5001, debug=True)

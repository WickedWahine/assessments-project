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
        flash(f"Welcome, {user.first_name} {user.last_name}!")

    return redirect("/")


@app.route("/logout")
def process_logout():
    """Log user out"""

    session.pop("username", None)
    flash("Logged out.")
    
    return redirect("/")


@app.route('/assessment/')
def students_by_teacher():

    assessment_name = request.args.get("assessment_name")
    grade = request.args.get("grade")
    school_id = request.args.get("school_id")
    print(assessment_name)

    # If no user is logged in, reject request
    if not session.get("username"):
        flash("Please log in first.")
        return redirect("/")

    username = session.get("username")
    user_id = crud.get_user_by_username(username).user_id

    # Temporarily hard code parameters
    test_school_id = 2
    test_grade = "1"
    test_academic_year_id = 5

    students = crud.get_student_roster_by_teacher(user_id, test_school_id, test_grade, test_academic_year_id)
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

    date_taken = date.today()
    
    teacher = {"first_name": request.form.get('teacher_first'),
                "last_name": request.form.get('teacher_last'),
                "username": request.form.get('teacher_username')}

    assessment_name = assessment_name

    # Find Assessment ID for this assessment
    assessment_id = crud.get_assessment_id_by_name(assessment_name).assessment_id

    # Given Assessment ID and date taken, get Scoring Term ID
    scoring_term_id = crud.get_scoring_term_by_assessement_id_and_date_taken(assessment_id, date_taken).scoring_term_id

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


# @app.route('/movies/<movie_id>/rate', methods=['POST'])
# def rate_movie(movie_id):
#     score = request.form.get('score')
#     movie = crud.get_movie_by_id(movie_id)
#     user = crud.get_user_by_id(session['id'])
    
#     if score.isdigit():
#         score_int = int(score)
#         if score_int > -1 and score_int < 101:
#             crud.create_rating(score, movie, user)
#             flash("Created rating!")
#         else:
#             flash("Rating not within valid range!")
#     else:
#         flash("Not an integer!")
#     return redirect('/')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0", port=5001, debug=True)

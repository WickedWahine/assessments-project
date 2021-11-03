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


@app.route('/bas')
def students_by_teacher():

    # Temporarily hard code parameters
    test_user_id = 49
    test_school_id = 2
    test_grade = "2"
    test_academic_year_id = 5

    students = crud.get_student_roster_by_teacher(test_user_id, test_school_id, test_grade, test_academic_year_id)
    students = [student.student for student in students]
    students.sort(key=lambda student: student.first_name)
    
    student_ass = [student.student_assessments for student in students]
    rosters = [student.rosters for student in students]
    teacher = crud.get_user_by_id(test_user_id)
    today = date.today().strftime("%m/%d/%y")

    return render_template('bas.html', students=students, rosters=rosters, teacher=teacher, student_ass=student_ass, today=today)


@app.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    user = crud.get_user_by_username(username)
    
    if password == user.password:
        session['id'] = user.user_id
        flash("Logged in!")
    else:
        flash("Authentication failed!")

    return redirect('/')

# @app.route('/<assessment_name>/entries', methods="GET")
# def get_assessment_results():


@app.route('/bas/entries', methods=['POST'])
def record_entries():

    date_taken = date.today()

    # Hard-coding Assessment name
    ass_name = "BAS"

    # Find Assessment ID for this assessment
    ass_id = crud.get_assessment_id_by_name(ass_name).assessment_id

    # Given Assessment ID and date taken, get Scoring Term ID
    scoring_term_id = crud.get_scoring_term_id_by_assessement_id_and_date_taken(ass_id, date_taken).scoring_term_id

    # for k, v in request.form.items():
    #     entry_dict.append({k: v})
    entries = []

    student_ids = request.form.getlist('student_id')
    scores = request.form.getlist('score')
    exemption_ids = request.form.getlist('exemption_id')

    for i, sid in enumerate(student_ids):
        entries.append({sid: {'student_id': sid, 'score': scores[i], 'exemption_id': exemption_ids[i]}})
    
    print(pprint(entries))

    # if score.isdigit():
    #     score_int = int(score)
    #     if score_int > -1 and score_int < 101:
    #         crud.create_rating(score, movie, user)
    #         flash("Created rating!")
    #     else:
    #         flash("Rating not within valid range!")
    # else:
    #     flash("Not an integer!")
    return redirect('/')


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

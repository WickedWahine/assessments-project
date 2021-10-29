"""Server for assessments app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
from jinja2 import StrictUndefined

import crud

app = Flask(__name__)
app.secret_key = 'VLF8AsFAy!qbrkdN6Ra$6F#-!UrNBT'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/students')
# def students_in_my_class(user_id):
#     rosters =  crud.get_roster_by_user_id(user_id)
#     rostered_students = crud.all_rostered_students()
#     return render_template('students.html', rosters=rosters, rostered_students=rostered_students)

def students_by_teacher():

    test_user_id = 49
    test_school_id = 2
    test_grade = "2"
    test_academic_year_id = 5

    students = crud.get_student_roster_by_teacher(test_user_id, test_school_id, test_grade, test_academic_year_id)
    students = [student.student for student in students]
    student_ass = [student.student_assessments for student in students]
    rosters = [student.rosters for student in students]
    teacher = crud.get_user_by_id(test_user_id)

    return render_template('students.html', students=students, osters=rosters, teacher=teacher, student_ass=student_ass)


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

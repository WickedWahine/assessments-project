"""
os
    This is a module from Python’s standard library. It contains code related to working with your computer’s operating system.

json
    Remember this module from the APIs lab? You’ll need this to load the data in data/academic_years.json.

datetime from datetime
    We’ll use datetime.strptime to turn a string into a Python datetime object.

crud, model, and server
    These are all files that you wrote (or will write) — crud.py, model.py, and server.py.
"""

import crud, model, server
import os, json
from datetime import datetime

os.system("dropdb assdb")
os.system("createdb assdb")

model.connect_to_db(server.app)
model.db.create_all()

# Load academic year data from JSON file
with open("data/academic_years.json") as f:
    academic_year_data = json.loads(f.read())

    # Create academic years, store them in list
    academic_years_in_db = []
    for academic_year in academic_year_data:

        year = academic_year["year"]
        start_date = datetime.strptime(academic_year["start_date"], "%m/%d/%Y")
        end_date = datetime.strptime(academic_year["end_date"], "%m/%d/%Y")

        academic_year = crud.create_academic_year(year, start_date, end_date)
        academic_years_in_db.append(academic_year)
    
    f.close()


# Load assessment data from JSON file
with open("data/assessments.json") as f:
    assessment_data = json.loads(f.read())

    # Create assessments, store them in list
    assessments_in_db = []
    for assessment in assessment_data:

        name = assessment["name"]
        subject = assessment["subject"]

        assessment = crud.create_assessment(name, subject)
        assessments_in_db.append(assessment)

    f.close()
        

# Load exemption data from JSON file
with open("data/exemptions.json") as f:
    exemption_data = json.loads(f.read())

    # Create exemptions, store them in list
    exemptions_in_db = []
    for exemption in exemption_data:

        reason = exemption["reason"]
        
        exemption = crud.create_exemption(reason)
        exemptions_in_db.append(exemption)
        
    f.close()


# Load role data from JSON file
with open("data/roles.json") as f:
    role_data = json.loads(f.read())

    # Create roles, store them in list
    roles_in_db = []
    for role in role_data:

        name = role["name"]
        description = role["description"]

        role = crud.create_role(name, description)
        roles_in_db.append(role)
        
    f.close()


# Load school data from JSON file
with open("data/schools.json") as f:
    school_data = json.loads(f.read())

    # Create schools, store them in list
    schools_in_db = []
    for school in school_data:

        name = school["name"]
        short_name = school["short_name"]
        letter_code = school["letter_code"]

        school = crud.create_school(name, short_name, letter_code)
        schools_in_db.append(school)
        
    f.close()


# Load student data from JSON file
with open("data/students.json") as f:
    student_data = json.loads(f.read())

    # Create students, store them in list
    students_in_db = []
    for student in student_data:

        student_id = student["student_id"]
        state_id = student["state_id"]
        first_name = student["first_name"]
        last_name = student["last_name"]

        student = crud.create_student(student_id, state_id, first_name, last_name)
        students_in_db.append(student)
        
    f.close()


# Load user data from JSON file
with open("data/users.json") as f:
    user_data = json.loads(f.read())

    # Create users, store them in list
    users_in_db = []
    for user in user_data:

        staff_id = user["staff_id"]
        first_name = user["first_name"]
        last_name = user["last_name"]
        username = user["username"]
        password = user["password"]
        role_id = user["role_id"]
       
        # bool("True") ---> True
        active_status = bool(user["active_status"])

        user = crud.create_user(staff_id, first_name, last_name, username, password, role_id, active_status)
        users_in_db.append(user)
        
    f.close()


# Load benchmark data from JSON file
with open("data/benchmarks.json") as f:
    benchmark_data = json.loads(f.read())

    # Create benchmarks, store them in list
    benchmarks_in_db = []
    for benchmark in benchmark_data:

        assessment_id = benchmark["assessment_id"]
        grade = benchmark["grade"]
        term = benchmark["term"]
        level = benchmark["level"]
        cutoff = benchmark["cutoff"]

        benchmark = crud.create_benchmark(assessment_id, grade, term, level, cutoff)
        
        benchmarks_in_db.append(benchmark)
        
    f.close()


# Load roster data from JSON file
with open("data/rosters.json") as f:
    roster_data = json.loads(f.read())

    # Create rosters, store them in list
    rosters_in_db = []
    for roster in roster_data:

        school_id = roster["school_id"]
        student_id = roster["student_id"]
        user_id = roster["user_id"]
        grade = roster["grade"]
        academic_year_id = roster["academic_year_id"]

        roster = crud.create_roster(school_id, student_id, user_id, grade, academic_year_id)
        rosters_in_db.append(roster)
        
    f.close()


# Load scoring term data from JSON file
with open("data/scoring_terms.json") as f:
    scoring_term_data = json.loads(f.read())

    # Create scoring_terms, store them in list
    scoring_terms_in_db = []
    for scoring_term in scoring_term_data:

        assessment_id = scoring_term["assessment_id"]
        academic_year_id = scoring_term["academic_year_id"]
        term = scoring_term["term"]

        date_open = datetime.strptime(scoring_term["date_open"], "%m/%d/%Y")
        date_close = datetime.strptime(scoring_term["date_close"], "%m/%d/%Y")

        scoring_term = crud.create_scoring_term(assessment_id, academic_year_id, term, date_open, date_close)
        scoring_terms_in_db.append(scoring_term)
        
    f.close()


# Load student assessment data from JSON file
with open("data/student_assessments.json") as f:
    student_assessment_data = json.loads(f.read())

    # Create student assessments, store them in list
    student_assessments_in_db = []
    for student_assessment in student_assessment_data:

        student_id = student_assessment["student_id"]
        scoring_term_id = student_assessment["scoring_term_id"]
        
        # cast to ensure empty strings are converted into int
        exemption_id = student_assessment["exemption_id"]
        score = student_assessment["score"]
        benchmark_id = student_assessment["benchmark_id"]
        date_taken = datetime.strptime(student_assessment["date_taken"], "%m/%d/%Y")

        student_assessment = crud.create_student_assessment(student_id, scoring_term_id,
                                                            exemption_id, score, 
                                                            benchmark_id, date_taken)
        student_assessments_in_db.append(student_assessment)
        
    f.close()
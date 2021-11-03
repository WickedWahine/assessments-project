"""CRUD operations."""

from model import (db, Academic_Year, Assessment, Benchmark, Exemption, Role,
                    Roster, School, Scoring_Term, Student, Student_Assessment,
                    User, connect_to_db)


def create_academic_year(year, start_date, end_date):
    """Create and return an academic year."""

    academic_year = Academic_Year(year=year,
                    start_date=start_date,
                    end_date=end_date)
    
    db.session.add(academic_year)
    db.session.commit()

    return academic_year

#create_academic_year("2025-2026", "2025-7-1", "2026-6-30")


def create_assessment(name, subject):
    """Create and return an assessment."""

    assessment = Assessment(name=name,
                    subject=subject)
    
    db.session.add(assessment)
    db.session.commit()

    return assessment

#create_assessment("TCW", "A literacy test in writing")


def create_benchmark(assessment_id, grade, term, level, cutoff):
    """Create and return a benchmark."""

    benchmark = Benchmark(
                    assessment_id = assessment_id,
                    grade=grade,
                    term=term,
                    level=level,
                    cutoff=cutoff)

    db.session.add(benchmark)
    db.session.commit()

    return benchmark

#create_benchmark(21, 5, "Fall", "", "G")


def create_exemption(reason):
    """Create and return an exemption."""

    exemption = Exemption(
                    reason=reason)

    db.session.add(exemption)
    db.session.commit()

    return exemption

#create_exemption("Test Reason")


def create_role(name, description):
    """Create and return a role."""

    role = Role(name=name,
                description=description)

    db.session.add(role)
    db.session.commit()

    return role

#create_role("Queen", "Can delegate everything to others :-)")


def create_roster(school_id, student_id, user_id, grade, academic_year_id):
    """Create and return a roster."""

    roster = Roster(school_id=school_id,
                    student_id=student_id,
                    user_id=user_id,
                    grade=grade,
                    academic_year_id=academic_year_id)

    db.session.add(roster)
    db.session.commit()

    return roster

#create_roster(26, 2700, 280, 5, "2025-2026")


def create_school(name, short_name, letter_code):
    """Create and return a benchmark."""

    school = School(name=name,
                    short_name=short_name,
                    letter_code=letter_code)

    db.session.add(school)
    db.session.commit()

    return school

#create_school("Hogwarts Academy", "Hogwarts", "HA")


def create_scoring_term(assessment_id, academic_year_id, term, date_open, date_close):
    """Create and return a scoring term."""

    scoring_term = Scoring_Term(assessment_id=assessment_id,
                    academic_year_id=academic_year_id,
                    term=term,
                    date_open=date_open,
                    date_close=date_close)

    db.session.add(scoring_term)
    db.session.commit()

    return scoring_term

#create_scoring_term(21, "2025-2026", "Fall", "8/1/2025", "11/30/2026")


def create_student(student_id, state_id, first_name, last_name):
    """Create and return a benchmark."""

    student = Student(student_id=student_id,
                    state_id=state_id,
                    first_name=first_name,
                    last_name=last_name)

    db.session.add(student)
    db.session.commit()

    return student

#create_student(1234567, 987654321, "Grace", "Hopper")


def create_student_assessment(student_id, scoring_term_id, exemption_id, score, benchmark_id, date_taken):
    """Create and return exemptions of an assessment for a given student."""

    student_assessment = Student_Assessment(
                    student_id=student_id,
                    scoring_term_id=scoring_term_id,
                    exemption_id=exemption_id,
                    score=score,
                    benchmark_id=benchmark_id,
                    date_taken=date_taken)
    
    db.session.add(student_assessment)
    db.session.commit()

    return student_assessment

#create_student_assessment(12, 40, 2, "subA", 3, "9/23/2000")


def create_user(staff_id, first_name, last_name, username, password, role_id, active_status):
    """Create and return a new user."""

    user = User(staff_id=staff_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                role_id=role_id,
                active_status=active_status)

    db.session.add(user)
    db.session.commit()

    return user

#create_user(3000, "Linus", "Pauling", "lpauling@fa.ke", "password", 24, True)



########## Get ALL records of a table ##########

def all_academic_years():
    """Query to list all academic years"""

    return Academic_Year.query.all()


def all_assessments():
    """Query to list all assessments"""

    return Assessment.query.all()


def all_benchmarks():
    """Query to list all benchmarks"""

    return Benchmark.query.all()


def all_exemptions():
    """Query to list all exemptions"""

    return Exemption.query.all()


def all_roles():
    """Query to list all roles"""

    return Role.query.all()


def all_rosters():
    """Query to list all rosters"""

    return Roster.query.all()


def all_schools():
    """Query to list all schools"""

    return School.query.all()


def all_scoring_terms():
    """Query to list all scoring terms"""

    return Scoring_Term.query.all()


def all_student_assessments():
    """Query to list all student assessments data"""

    return Student_Assessment.query.all()


def all_students():
    """Query to list all students"""

    return Student.query.all()


def all_users():
    """Query to list all users"""

    return User.query.all()



########## Get record by a parameter ##########

def get_assessment_id_by_name(name):
    """Query assessment ID by its name"""

    return Assessment.query.filter(Assessment.name==name).one()


def get_scoring_term_by_assessement_id_and_date_taken(assessment_id, date_taken):  
    """Query scoring term ID by assessment ID and date taken"""

    scoring_term_id = (Scoring_Term.query
                        .filter(Scoring_Term.assessment_id==assessment_id, Scoring_Term.date_open<=date_taken, Scoring_Term.date_close>=date_taken)
                        .one())

    return scoring_term_id


def get_user_by_username(username):
    """Query user ID by username"""

    return User.query.filter(User.username==username).one()


def get_benchmark_by_id(id):
    """Query benchmark by ID"""

    return Benchmark.query.get(id)


def get_role_by_id(id):
    """Query role by ID"""

    return Role.query.get(id)


def get_student_roster_by_teacher(user_id, school_id, grade, academic_year_id):
    """ Query to list students by teacher, school, grade, academic year.
        Since roster is what ties then tgt, we use the object Roster.
    """

    student_roster = (Roster.query
                    .filter_by(user_id=user_id, school_id=school_id, grade=grade, academic_year_id=academic_year_id)
                    .all())

    return student_roster


def get_school_by_id(id):
    """Query school by ID"""

    return School.query.get(id)


def get_student_assessment_by_id(id):
    """Query student by ID"""

    return Student_Assessment.query.get(id)


def get_student_by_id(id):
    """Query student by ID"""

    return Student.query.get(id)


def get_assessment_by_name(name):
    """Query user by name"""

    return Assessment.query.filter_by(name=name).first()



########## Get zero or just the first record by a parameter ##########

def get_academic_year_by_year(year):
    """Query academic year by year"""

    return Academic_Year.query.filter_by(year=year).first()


def get_assessment_by_name(name):
    """Query assessment by name"""

    return Assessment.query.filter_by(name=name).first()


def get_role_by_name(name):
    """Query role by name"""

    return Role.query.filter_by(name=name).first()


def get_school_by_short_name(short_name):
    """Query user by short name"""

    return School.query.filter_by(short_name=short_name).first()


def get_school_by_letter_code(letter_code):
    """Query user by letter code"""

    return School.query.filter_by(letter_code=letter_code).first()
    

def get_student_by_student_id(student_id):
    """Query user by student ID"""

    return Student.query.filter_by(student_id=student_id).all()



########## Get ALL records filtered by various parameter ##########

def get_roster_by_academic_year(academic_year):
    """Query rosters by academic_year"""

    return Roster.query.filter_by(academic_year=academic_year)


def get_roster_by_grade(grade):
    """Query rosters by grade"""

    return Roster.query.filter_by(grade=grade)


def get_roster_by_school_id(school_id):
    """Query rosters by school_id"""

    return Roster.query.filter_by(school_id=school_id)


def get_roster_by_school_name(school_name):
    """Query rosters by school_name"""

    return Roster.query.filter_by(school_name=school_name)


def get_roster_by_school_short_name(school_short_name):
    """Query rosters by school_short_name"""

    return Roster.query.filter_by(school_short_name=school_short_name)


def get_roster_by_school_letter_code(school_letter_code):
    """Query rosters by school_letter_code"""

    return Roster.query.filter_by(school_letter_code=school_letter_code)


def get_scoring_term_by_academic_year_id(academic_year_id):
    """Query scoring_terms by academic_year_id"""

    return Scoring_Term.query.filter_by(academic_year_id=academic_year_id)


def get_student_assessment_by_scoring_term_id(scoring_term_id):
    """Query student_assessments by scoring_term_id"""

    return Student_Assessment.query.filter_by(scoring_term_id=scoring_term_id)


def get_student_assessment_by_student_id(student_id):
    """Query student_assessments by student_id"""

    return Student_Assessment.query.filter_by(student_id=student_id)


def get_user_by_role_id(role_id):
    """Query user by role ID"""

    return User.query.filter_by(role_id=role_id)


def get_user_by_active_status(active_status):
    """Query user by status"""

    return User.query.filter_by(active_status=active_status)



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
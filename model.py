"""Models for assessments app."""

from datetime import datetime
#from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Academic_Year(db.Model):
    """An academic year."""

    __tablename__ = "academic_years"

    academic_year_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    year = db.Column(db.String, unique=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    # Note: academic_year = db.relationship("Academic_Year", backref="scoring_terms")

    def __repr__(self):
        return f'<Academic_Year academic_year_id={self.academic_year_id} year={self.year} start_date={self.start_date} end_date={self.end_date}>'


class Assessment(db.Model):
    """An assessment."""

    __tablename__ = "assessments"

    assessment_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)
    subject = db.Column(db.String)

    # Note: assessment = db.relationship("Assessment", backref="scoring_terms")
    # Note: assessment = db.relationship("Assessment", backref="benchmark")

    def __repr__(self):
        return f'<Assessment assessment_id={self.assessment_id} name={self.name} subject={self.subject}>'


class Benchmark(db.Model):
    """A benchmark."""

    __tablename__ = "benchmarks"

    benchmark_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    assessment_id = db.Column(db.Integer,db.ForeignKey('assessments.assessment_id'))
    grade = db.Column(db.String, nullable=False)
    term = db.Column(db.String, nullable=False)
    level = db.Column(db.String)
    cutoff = db.Column(db.String)

    assessment = db.relationship("Assessment", backref="benchmark")

    def __repr__(self):
        return f'<Benchmark grade={self.grade} term={self.term} level={self.level} cutoff={self.cutoff} assessment_id={self.assessment_id}>'


class Exemption(db.Model):
    """A exemption."""

    __tablename__ = "exemptions"

    exemption_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    reason = db.Column(db.String, unique=True)

    # Note: examption = db.relationship("Exemption", backref="student_assessments")

    def __repr__(self):
        return f'<Exemption exemption_id={self.exemption_id} reason={self.reason}>'


class Role(db.Model):
    """A user role, determines access."""

    __tablename__ = "roles"

    role_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text) #To document what each role can or cannot do

    # Note: role = db.relationship("Role", backref="users")

    def __repr__(self):
        return f'<Role role_id={self.role_id} name={self.name} description={self.description}>'


class Roster(db.Model):
    """A list of students enrolled in a section and who's teaching it."""

    __tablename__ = "rosters"

    roster_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.school_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    grade = db.Column(db.String, nullable=False)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.academic_year_id'))

    school = db.relationship("School", backref="rosters")
    student = db.relationship("Student", backref="rosters")
    user = db.relationship("User", backref="rosters")

    def __repr__(self):
        return f'<Roster school_id={self.school_id} student_id={self.student_id} user_id={self.user_id} grade={self.grade} academic_year_id={self.academic_year_id}>'


class School(db.Model):
    """A school."""

    __tablename__ = "schools"

    school_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String, unique=True)
    short_name = db.Column(db.String, unique=True)
    letter_code = db.Column(db.String, unique=True)

    # Note: school = db.relationship("School", backref="rosters")
    
    def __repr__(self):
        return f'<School school_id={self.school_id} name={self.name} short_name={self.short_name}>'


class Scoring_Term(db.Model):
    """A time window when teachers can enter scores."""

    __tablename__ = "scoring_terms"

    scoring_term_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.assessment_id'))
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.academic_year_id'))
    term = db.Column(db.String)
    date_open = db.Column(db.DateTime)
    date_close = db.Column(db.DateTime)

    # Note: scoring_term = db.relationship("Scoring_Term", backref="student_assessments")
    
    assessment = db.relationship("Assessment", backref="scoring_terms")
    academic_year = db.relationship("Academic_Year", backref="scoring_terms")

    def __repr__(self):
        return f'<Scoring_Term scoring_term_id={self.scoring_term_id} assessment_id={self.assessment_id} academic_year_id={self.academic_year_id} term={self.term} date_open={self.date_open}>'


class Student(db.Model):
    """A student."""

    __tablename__ = "students"

    student_id = db.Column(db.Integer,
                        #autoincrement=True,
                        primary_key=True)
    #local_id = db.Column(db.Integer, unique=True)
    state_id = db.Column(db.BigInteger, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # Note: student = db.relationship("Student", backref="rosters")
    # Note: student = db.relationship("Student", backref="student_assessments")

    def __repr__(self):
        return f'<Student first_name={self.first_name} last_name={self.last_name}>'


class Student_Assessment(db.Model):
    """A student assessment details."""

    __tablename__ = "student_assessments"

    student_assessment_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    scoring_term_id = db.Column(db.Integer, db.ForeignKey('scoring_terms.scoring_term_id'))
    exemption_id = db.Column(db.Integer, db.ForeignKey('exemptions.exemption_id'), nullable=True)
    score = db.Column(db.String)
    benchmark_id = db.Column(db.Integer)
    date_taken = db.Column(db.Date)

    # Note: student = db.relationship("Student", backref="rosters")

    scoring_term = db.relationship("Scoring_Term", backref="student_assessments")
    student = db.relationship("Student", backref="student_assessments")
    exemption = db.relationship("Exemption", backref="student_assessments")

    def __repr__(self):
        return f'<Student_Assessment student_id={self.student_id} scoring_term_id={self.scoring_term_id} exemption_id={self.exemption_id} score={self.score} date_taken={self.date_taken}>'


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    staff_id = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    active_status = db.Column(db.Boolean)

    role = db.relationship("Role", backref="users")

    # Note: user = db.relationship("User", backref="rosters")

    def __repr__(self):
        return f'<User first_name={self.first_name} username={self.username}>'


def connect_to_db(flask_app, db_uri="postgresql:///assdb", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)
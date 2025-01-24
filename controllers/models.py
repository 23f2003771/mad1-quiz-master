from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users_Info(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    qualifications = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.DATE() , nullable=False)


class Subjects(db.Model):
    __tablename__ = 'subjects'
    Subject_code = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    subject_name = db.Column(db.String(80), nullable=False)
    subject_description = db.Column(db.String(120), nullable=False)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    question_statement = db.Column(db.String(80), nullable=False)
    option1 = db.Column(db.String(80), nullable=False)
    option2 = db.Column(db.String(80), nullable=False)
    option3 = db.Column(db.String(80), nullable=False)
    option4 = db.Column(db.String(80), nullable=False)
    correct_answer = db.Column(db.String(80), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)
    Chapter = db.relationship('Chapter', backref=('questions'), lazy=True)


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date_of_quiz = db.Column(db.DATE(), nullable=False)
    time_duration = db.Column(db.TIME(), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)
    Chapter = db.relationship('Chapter', backref=('quiz'), lazy=True)

class Chapter(db.Model):
    __tablename__ = 'chapter'
    chapter_id = db.Column(db.Integer, primary_key=True,unique=True,nullable=False)
    chapter_name = db.Column(db.String(80), nullable=False,autoincrement=True)
    chapter_description = db.Column(db.String(120), nullable=False)
    subject_code_chapter = db.Column(db.Integer,nullable=False)

class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DATETIME(), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    user = db.relationship('Users_Info', backref=('scores'), lazy=True)
    quiz = db.relationship('Quiz', backref=('scores'), lazy=True)
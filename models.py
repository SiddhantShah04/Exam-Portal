from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registration(db.Model):
    __tablename__ = "Registration"
    Email = db.Column(db.String, nullable=False,primary_key=True)
    Password = db.Column(db.String, nullable=False)

    def add_Exam(self,branch,sem,subject):
        addE = Exam(branch=branch,sem=sem,subject=subject,Email=self.Email)
        db.session.add(addE)
        db.session.commit()

    def add_Question(self,Question,option1,option2,option3,option4,answer,Time,subject):
        add_Q=Quest(Question=Question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,Time=Time,subject=subject)
        db.session.add(add_Q)
        db.session.commit()


class Exam(db.Model):
    __tablename__ = "Exam"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    branch = db.Column(db.String, nullable=False)
    sem = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False,primary_key=True)
    Email = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=True)


class Quest(db.Model):
    __tablename__ = "Quest"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Question = db.Column(db.String, nullable=False)
    option1 = db.Column(db.String,nullable=False)
    option2 = db.Column(db.String,nullable=False)
    option3 = db.Column(db.String,nullable=False)
    option4 = db.Column(db.String,nullable=False)
    answer = db.Column(db.String,nullable=False)
    Time = db.Column(db.Integer,nullable=False)
    subject = db.Column(db.String,nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    imageTOrF = db.Column(db.String, nullable=True)

class students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    SubjectRoll = db.Column(db.String, nullable=False)

class Result(db.Model):
    __tableanme__="Result"
    id = db.Column(db.Integer,primary_key=True)
    roll = db.Column(db.Integer,nullable=False)
    correctAnswers = db.Column(db.Integer,nullable=False)
    subjectName = db.Column(db.String,nullable=False)



from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,send_file
import os,shutil
import csv
import json
from sqlalchemy.sql import func
import logging
from models import *


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.secret_key = "E"


app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def index():
    activeSubject = Exam.query.filter_by(status="active").all()
    return render_template("index.html",activeSubject=activeSubject)

@app.route("/logout")
def logout():
    if('Email' in session):
        session.pop('Email',None)
        return redirect(url_for("index"))
    else:
        return("<h4>You already logout</h4>")


@app.route("/CreateAccount",methods=["Post","GET"])
def Create_Account():
    return render_template("CreateAccount.html")


@app.route("/signUp",methods=["POST"])
def signUp():
    E = request.form.get("EMAIL")
    P = request.form.get("PASSWORD")
    try:
        Resgistrated = Registration(Email=E,Password=P)
        db.session.add(Resgistrted)
        db.session.commit()
        return render_template("index.html")
    except:
        Error = "Already have an account with this Email ID."
        return render_template("CreateAccount.html",Error=Error)


@app.route("/ProfessorZone",methods=["POST"])
def ProfessorZone():
    if(request.method == "POST"):
        E = request.form.get("Email")
        session['Email']=E
        P = request.form.get("Password")
        result = Registration.query.filter_by(Password=P,Email=E).first()
        print(result)
        if(result != None):
            return redirect(url_for('Email',Email=E))
        else:
            Error =  "Invalid email or password"
            return render_template("index.html",Error=Error)
    else:
        return render_template("Professors.html")

@app.route('/Email/<string:Email>',methods=["POST","GET"])
def Email(Email):
    if('Email' in session):
        E=Exam.query.filter_by(Email=Email).all()
        return render_template("Professors.html",Email=Email,E=E)
    else:
        return render_template("index.html")

@app.route("/<string:Email>/Create_Question",methods=["POST","GET"])
def Create_Question(Email):
    if('Email' in session):
        return render_template("question.html",Email=Email)
    else:
        return render_template("index.html")

@app.route("/<string:Email>/uploader",methods=["POST","GET"])
def uploader(Email):
    if('Email' in session):
        f = request.files['file']
        f.save(os.path.join('UploadFiles',f.filename))
        Branch = request.form.get("Branch")
        Sem = request.form.get("Sem")
        #Subject = (request.form.get("Subject").replace(" ",""))
        subject = request.form.get("Subject")
        FileName = (f.filename)
        t=Exam.query.filter_by(Email=Email).first()
        if(t==None):
            t = Registration.query.filter_by(Email=Email).first()
            t.add_Exam(branch=Branch,sem=Sem,subject=subject)

        elif(t.subject == subject ):
            error="Question Paper with this subject name already exist"
            return render_template("question.html",Email=Email,error=error)
        else:
            t = Registration.query.filter_by(Email=Email).first()
            t.add_Exam(branch=Branch,sem=Sem,subject=subject)

        with open(f"UploadFiles/{FileName}", 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            for Question,option1,option2,option3,option4,answer,Time in csvreader:
                t.add_Question(Question=Question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,Time=Time,subject=subject)
        return redirect(url_for('Email',Email=Email))
    else:
        return render_template("index.html")



@app.route("/<string:r>/delete",methods=["POST","GET"])
def delete(r):
    if('Email' in session):
        Email = session['Email']
        delE=Exam.query.filter_by(subject=r).first()
        delet = Quest.query.filter_by(subject=r).all()
        for i in delet:
            db.session.delete(i)
        db.session.delete(delE)
        db.session.commit()

        return redirect(url_for('Email',Email=Email))
    else:
        return render_template("index.html")


@app.route("/<string:Email>/<string:r>/Deploy",methods=["POST","GET"])
def Deploy(Email,r):
    examStatus=Exam.query.filter_by(subject=r).first()
    examStatus.status = "active"
    db.session.commit()
    #return("<h1 style='text-align:center;'>Already activated!</h1>")
    return redirect(url_for('Email',Email=Email))

@app.route("/StudentZone",methods=["POST","GET"])
def StudentZone():
    errorStudent=None
    Roll = request.form.get("Roll")
    Subject = request.form.get("Subject")
    SubjectResult=f'{Subject}'+'Result'
    if(Roll== "" or Subject==""):
        errorStudent="Check your Roll and subject"
        return render_template("index.html",errorStudent=errorStudent)
    #questionPaper = Quest.query.filter_by(subject=Subject).all()
    questionPaper=Quest.query.order_by(func.random()).all() # for PostgreSQL, SQLite
    #questionPaper = Quest.query.filter_by(subject=Subject).all()
    for Question in questionPaper:
        print(Question.Question)
    return("ok")

"""
    if(f'{Roll}' in session):
        session.pop(f'{Roll}',None)
        return("<h1>already taken</h1>")
    session[f"{Roll}"] = 0
    s=1
    db.execute('create table if not exists ":SubjectName"("Roll" smallint not null,"Right" smallint not null)',{"SubjectName":SubjectResult})
    i=0
    try:
        db.execute('insert into ":SubjectName" ("Roll","Right") values(:Roll,:i)',{"SubjectName":SubjectResult,"Roll":Roll,"i":i})
        db.commit()
    except:
        db.rollback()
    rows = E[session[f"{Roll}"]]
    return render_template("Paper.html",Subject=Subject,rows=rows,Roll=Roll,l=l,s=s)
"""

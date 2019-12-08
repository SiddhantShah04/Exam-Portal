from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,send_file,jsonify
import os,shutil
import csv
import json
from base64 import b64encode
import base64
from sqlalchemy.sql import func
from models import *
#readme file
#flask run --host=0.0.0.0

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://axynzjdefwmyeo:e87f02858c1fbc56ea43154a07967f3d68c6e4ad7766daeee3eccc352380caa1@ec2-174-129-253-62.compute-1.amazonaws.com:5432/dcmaleb1aubmap"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key = "f*"


app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index2():

    activeSubject = Exam.query.filter_by(status="active").all()

    return render_template("index2.html",activeSubject=activeSubject)

@app.route("/logout")
def logout():
    if('Email' in session):
        session.pop('Email',None)
        return redirect(url_for("index2"))
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
        db.session.add(Resgistrated)
        db.session.commit()
        return render_template("index2.html")
    except:
        Error = "Already have an account with this Email ID."
        return render_template("index2.html",Error=Error)


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
            return render_template("index2.html",Error=Error)
    else:
        return render_template("Professors.html")

@app.route("/Email",methods=["POST","GET"])
def Professor():
    if('Email' in session):
        E=session['Email']
        return redirect(url_for('Email',Email=E))
    else:
        return render_template("index2.html")

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
        subject = request.form.get("Subject")
        try:
            os.mkdir(subject)
        except:
            pass
        f.save(os.path.join(f'{subject}',f.filename))
        Branch = request.form.get("Branch")
        Sem = request.form.get("Sem")
        FileName = (f.filename)
        t=Exam.query.all()
        for i in t:
            if(i.subject==subject):
                error="Question Paper with this subject name already exist"
                return render_template("question.html",Email=Email,error=error)
        t = Registration.query.filter_by(Email=Email).first()
        t.add_Exam(branch=Branch,sem=Sem,subject=subject)
        with open(f"{subject}/{FileName}",'r', encoding='ISO-8859-1') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)

            for Question,option1,option2,option3,option4,answer,Time in csvreader:
                t.add_Question(Question=Question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,Time=Time,subject=subject)

        return redirect(url_for('Email',Email=Email))
    else:
        return render_template("index.html")


@app.route("/<string:r>/delete",methods=["POST","GET"])
def delete(r):
    if('Email' in session):
        try:
            shutil.rmtree(f'{r}')
            os.remove(f'Results/{r}.csv')
        except:
            pass
        Email = session['Email']
        delE=Exam.query.filter_by(subject=r).first()
        delet = Quest.query.filter_by(subject=r).all()
        student =students.query.filter_by(Subject=r).all()
        dResult = Result.query.filter_by(subjectName=r).all()
        for i in delet:
            db.session.delete(i)
        for j in dResult:
            db.session.delete(j)
        for k in student:
            db.session.delete(k)
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
    return redirect(url_for('Email',Email=Email))

@app.route("/<string:r>/activateUsers",methods=["POST","GET"])
def activateUsers(r):
    print(r)
    student =students.query.filter_by(Subject=r).all()
    #make  a subject column then
    #to open adminier search roll
    for i in student:
        print(i.roll)
    return render_template("ActiveStudents.html",student=student,Subject=r)

@app.route("/remove/<string:subject>/<string:roll>",methods=["POST","GET"])
def remove(subject,roll):
    student =students.query.filter_by(Subject=subject,roll=roll).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('activateUsers',r=subject))

app.route("/error",methods=["GET"])
def error():
    errorStudent="Check your Roll and subject"
    activeSubject = Exam.query.filter_by(status="active").all()
    return render_template("index.html",errorStudent=errorStudent,activeSubject=activeSubject)


@app.route("/Activate/<string:subjectroll>",methods=["POST","GET"])
def Activate(subjectroll):
    print(subjectroll)
    student =students.query.filter_by(SubjectRoll=subjectroll).first()
    print(student)
    if(student == None):
        return  jsonify("true")
    else:
        print("False")
        return(jsonify("false"))

@app.route("/StudentZone/<string:r>",methods=["POST","GET"])
@app.route("/StudentZone",methods=["POST","GET"])
def StudentZone(r=None):
    errorStudent=None
    Roll = request.form.get("Roll")
    error = request.get_json()
    Subject = request.form.get("Subject")
    activeSubject = Exam.query.filter_by(status="active").all()

    addMarks = Result.query.filter_by(roll=Roll,subjectName=Subject).first()
    SubjectRoll=f"{Subject}{Roll}"
    if(Roll== "" or Subject==""):
        errorStudent="Check your Roll and subject"
        return render_template("index2.html",errorStudent=errorStudent,activeSubject=activeSubject)

    student =students.query.filter_by(SubjectRoll=SubjectRoll).first()
    #had given the exam

    if(student!= None and Roll != r):
        errorStudent = "Given roll number is already taken by a user"
        return render_template("index2.html",errorStudent=errorStudent,activeSubject=activeSubject)

    if(addMarks != None):
        errorStudent = "Exam of given roll number is already been done"
        return render_template("index2.html",errorStudent=errorStudent,activeSubject=activeSubject)

    if(r!=Roll):
        add_S=students(SubjectRoll=SubjectRoll,Subject=Subject,roll=Roll)
        db.session.add(add_S)
        db.session.commit()

    questionPaper=Quest.query.filter_by(subject=Subject).order_by(func.random()).all()
    t = Quest.query.filter_by(imageTOrF="T").all()
    images={}
    for i in t:
        image = base64.b64encode(i.image).decode('ascii')
        images[i.Question]=image
    #images.items() return a key and value of dict
    return render_template("Paper.html",questionPaper=questionPaper,Roll=Roll,data = images.items())

@app.route("/editQuestion/<string:subject>",methods=["POST","GET"])
def editQuestion(subject):
    Subject=subject
    questionPaper=Quest.query.filter_by(subject=Subject,imageTOrF = None).all()
    return render_template("editPaper.html",questionPaper=questionPaper,Subject=Subject)


@app.route("/addImage/<string:Subject>/<string:question>",methods=["POST"])
def addImage(Subject,question):
    Email = session['Email']
    Subject=Subject
    files = request.files.get('file')
    event = files.read()
    question=question
    print(question+"?")

    try:
        i=Quest.query.filter_by(Question=question+"?").first()
        i.image=event
        i.imageTOrF="T"
    except:
        i=Quest.query.filter_by(Question=question).first()
        i.image=event
        i.imageTOrF="T"

    db.session.commit()
    questionPaper=Quest.query.filter_by(subject=Subject,imageTOrF = None ).all()
    return redirect(url_for('editQuestion',subject=Subject))


@app.route("/<string:subject>/doneExam/<string:Roll>",methods=["POST","GET"])
def doneExam(subject,Roll):
    roll = Roll
    res = request.get_json()
    allColumns=Quest.query.all()
    count=0
    for ans in res:
        for key,value in ans.items():
            try:
                rows=Quest.query.filter_by(Question=key).first()
                if(ans[key] == rows.answer):
                    count=count+1
            except:
                pass
    SubjectRoll=f"{subject}{Roll}"
    student =students.query.filter_by(SubjectRoll=SubjectRoll).first()
    db.session.delete(student)
    db.session.commit()
    addMarks = Result(roll=roll,correctAnswers=count,subjectName=subject)
    db.session.add(addMarks)
    db.session.commit()
    return render_template('index.html')

@app.route("/<string:Email>/<string:Subject>/SeeResult",methods=["POST","GET"])
def SeeResult(Email,Subject):
    if('Email' in session):
        SubjectResult=f'{Subject}'+'Result'
        r=Result.query.filter_by(subjectName=Subject).order_by(Result.roll).all()
        fields = ['Roll','Total right answer']
        rows = []
        for i in r:
            rows.append([i.roll,i.correctAnswers])
        filename = f"Results/{Subject}.csv"
        with open(filename,'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(rows)
        path = f"{filename}"
        return send_file(path, as_attachment=True)
    else:
        return render_template('index.html')

@app.route("/downloadCsv",methods=["POST","GET"])
def downloadResult():
    if('Email' in session):
        fields = ['Question','Option1','Option2','Option3','Option4','Answer','Time in Second']
        filename= "QuestionPaper.csv"
        with open(filename,'w',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
        return send_file(filename,as_attachment=True)
    else:
        return render_template('index.html')

@app.errorhandler(500)
def error_500(exception):
    return ("<h1>Something went wrong.....try refreshing the page or Go back to previous page</h1>")

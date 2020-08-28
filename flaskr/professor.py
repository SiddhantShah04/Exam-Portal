import functools
from flask import (Blueprint,g,Flask,redirect,render_template,session,request,url_for,send_file,flash)
from werkzeug.exceptions import abort
import os,shutil
import json
import csv
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('professor',__name__)

@bp.route("/professor",methods=["GET","POST"])
@login_required
def professor():
    db = get_db()
    sql = "SELECT * FROM public.EXAM WHERE userID=(%s)"
    data = (session.get('user_id'),)
    cur = db.cursor()
    cur.execute(sql,data)
    Exam = cur.fetchall() 
    return render_template("Professors.html",Exam=Exam)

@bp.route("/status",methods=["GET","POST"])
@login_required
def status():
    db = get_db()
    cur = db.cursor()
    res = request.get_json()
    sql2 = "SELECT status from public.Exam where  id= (%s)"
    data = (res["examId"],)
    cur.execute(sql2,data)
    status = cur.fetchone()
    if(status[0] == "Active"):
        sql = "UPDATE public.Exam SET status='Deactive' where id = (%s); "
        result = "Deactive"
    else:
        sql = "UPDATE public.Exam SET status='Active' where id = (%s); "
        result = "Active"
    cur.execute(sql,data)
    db.commit()
    return(result)

@bp.route("/delete",methods=["GET","POST"])
@login_required
def delete():
    db = get_db()
    cur = db.cursor()
    res = request.get_json()
    data = (res["subject"],session.get('user_id'))
    # deleting all images of this exam question from folder
    sql3 = "SELECT Image FROM public.QuestionData WHERE subject= (%s) and userId = (%s) and Image is not null"
    cur.execute(sql3,data)
    imagesNames= cur.fetchall()
    for elt in imagesNames:
        print(elt[0])
        if(elt[0] is not None):
            os.remove(f"flaskr/templates/images/{elt[0]}")
    sql2 = "DELETE  from public.QuestionData WHERE subject= (%s) and userId = (%s)"
    cur.execute(sql2,data)
    sql = "DELETE  from public.Exam WHERE id= (%s) and userID=(%s)"
    data = (res["examId"],session.get('user_id'))
    cur.execute(sql,data)
    db.commit()
    return("Deleted")

@bp.route("/downloadCsv",methods=["GET","POST"])
@login_required
def downloadCsv():
    fields = ['Question','Option1','Option2','Option3','Option4','Answer','Time in Second']
    filename= "\QuestionPaper.csv"
    with open(filename,'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
    return send_file(filename,as_attachment=True)

@bp.route("/upload",methods=["GET","POST"])
@login_required
def upload():
    return render_template("question.html")

@bp.route("/editPaper",methods=["POST","GET"])
@login_required
def editpaper():
    db = get_db()
    cur = db.cursor()
    user_id = session.get('user_id')
    res = request.get_json()
    sql = "SELECT * FROM public.QuestionData WHERE userID = (%s) and subject = (%s) and Image is Null "
    data = (session.get("user_id"),res["subject"],)
    cur.execute(sql,data)
    result = cur.fetchall()
    
    result=json.dumps(result)
    return(result)

@bp.route("/uploadImage",methods=["POST","GET"])
@login_required
def uploadImage():
    qId = request.args.get('id')
    files = request.files['photo']
    files.save(os.path.join('flaskr/templates/images',qId+files.filename))
    db = get_db()
    cur = db.cursor()
    sql = "UPDATE public.QuestionData SET Image=(%s) WHERE id=(%s) and userId = (%s)"
    data = (qId+files.filename,qId,session.get("user_id"))
    cur.execute(sql,data)
    db.commit()
    result=json.dumps("Saved")
    return(result)

@bp.route("/uploadQuestion",methods=["GET","POST"])
@login_required
def uploadQuestion():
    db = get_db()
    cur = db.cursor()   
    subject = request.form["Subject"]
    Branch = request.form["Branch"]
    Sem = request.form["Sem"]
    f = request.files['file']
    id = session.get("user_id")
    try:
        os.mkdir(f'userId{id}')
    except:
        pass
    sql = "SELECT * FROM public.EXAM WHERE userID = (%s) and subject = (%s)"
    data = (session.get("user_id"),subject)
    cur.execute(sql,data)
    result = cur.fetchall()
    
    if(len(result) != 0):
            error = f"Questions of this {subject} is already uploaded."        
            flash(error)
            return render_template("question.html")
    f.save(os.path.join(f'userId{id}',f.filename))
    i = 1
    sql = "INSERT INTO public.QuestionData(userId,Subject,Question,Options,Answer,Time) VALUES(%s,%s,%s,%s,%s,%s)"
    sql2 = "INSERT INTO public.EXAM(branch,Semester,Subject,userID,status) VAlUES(%s,%s,%s,%s,%s)"
    
    try:
        with open(f"userId{id}/{f.filename}",'r', encoding='ISO-8859-1') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for Question,option1,option2,option3,option4,answer,Time in csvreader:
                data =(session.get('user_id'),subject,str(Question),[str(option1),str(option2),str(option3),str(option4)],str(answer),str(Time))
                try:
                    cur.execute(sql,data)
                    i=i+1
                except:
                    error = f"Some column of row {i} is missing, else check your file and try again"        
                    flash(error)
                    return render_template("question.html")
    except:
        error = "Only .Csv file are allowed to upload.Please check your file format"
        flash(error)
        return render_template("question.html")
    shutil.rmtree(f'userId{id}')
    data = (Branch,Sem,subject,session.get('user_id'),"Deactive")
    cur.execute(sql2,data)
    
    db.commit()
    return redirect(url_for("professor.professor"))        

@bp.route("/logged",methods=["GET","POST"])
def logged():
    db = get_db()
    cur = db.cursor()
    res = request.get_json()
    sql = "SELECT * FROM public.activeStudents WHERE examId=(%s)"
    data = (res["examId"],)
    cur.execute(sql,data)
    result = cur.fetchall()
    print(result)
    result=json.dumps(result)
    return(result)

@bp.route("/removeStudent",methods=["GET","POST"])
def removeStudent():
    res = request.get_json()
    db = get_db()
    cur = db.cursor()
    print(res)
    sql = "DELETE FROM public.activeStudents WHERE id=(%s)"
    data = (res["id"],)
    cur.execute(sql,data)
    db.commit()
    return("Done")

@bp.errorhandler(500)
def error_500(exception):
    return ("<h1>Something went wrong.....try refreshing the page or Go back to previous page</h1>")

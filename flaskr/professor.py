import functools
from flask import (Blueprint,g,Flask,redirect,render_template,request,url_for,send_file,flash)
from werkzeug.exceptions import abort
import os,shutil
import pandas as pd
import csv
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('professor',__name__)

@bp.route("/professor",methods=["GET","POST"])
@login_required
def professor():
    db = get_db()
    return render_template("Professors.html")

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

@bp.route("/uploadQuestion",methods=["GET","POST"])
@login_required
def uploadQuestion():
    db = get_db()
    cur = db.cursor()   
    subject = request.form["Subject"]
    Branch = request.form["Branch"]
    Sem = request.form["Sem"]
    f = request.files['file']
    try:
            os.mkdir(subject)
    except:
        pass

    f.save(os.path.join(f'{subject}',f.filename))
    i = 1
    sql = "INSERT INTO public.QuestionData(Subject,Question,Options,Answer,Time) VALUES(%s,%s,%s,%s,%s)"
    
    try:
        #    df = pd.read_csv(request.files["file"],encoding= 'unicode_escape')
        with open(f"{subject}/{f.filename}",'r', encoding='ISO-8859-1') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for Question,option1,option2,option3,option4,answer,Time in csvreader:
                data =(subject,str(Question),[str(option1),str(option2),str(option3),str(option4)],str(answer),str(Time))
            try:
                cur.execute(sql,data)
                db.commit()
                i=i+1
            except:
                error = f"Some column of row {i} is missing, else check your file and try again"        
                flash(error)
                return render_template("question.html")
    except:
        error = "Only .Csv file are allowed to upload.Please check your file format"
        flash(error)
        return render_template("question.html")
    #for i in df.itertuples():
    
    shutil.rmtree(f'{subject}')
    return render_template("professors.html")        
    

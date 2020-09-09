from flask import (Blueprint,g,Flask,redirect,render_template,request,url_for,flash)
from werkzeug.exceptions import abort
import json

bp = Blueprint('student',__name__,url_prefix='/student')
from flaskr.auth import login_required
from flaskr.db import get_db

@bp.route("/home",methods=["POST"])
def home():
    Roll = request.form.get("Roll")
    Subject = request.form.get("subject")
    
    sql = "SELECT * FROM public.activeStudents WHERE roll=(%s)"
    db = get_db()
    data = (Roll,)
    cur = db.cursor()
    cur.execute(sql,data)
    result = cur.fetchone()
    if(not result):
        return redirect(url_for('home.index'))
    
    sql = "SELECT id,Subject,Question,Option1,Option2,Option3,Option4,Image,Time FROM public.QuestionData WHERE subject=(%s) order by random()"
    data = (Subject,)
    cur.execute(sql,data)
    result = cur.fetchall()
    #result = json.dumps(result)
   
    return render_template("paper.html",result=result,Roll=Roll)

@bp.route("/submitAnswer",methods=["POST"])
def submitAnswer():
    res = request.get_json()

    db = get_db()
    sql2 = "SELECT id FROM public.Exam WHERE subject=(%s)"
    data = (res['subject'],)
    cur = db.cursor()
    cur.execute(sql2,data)
    examIds = cur.fetchone()
    count = 0
    for keys,value in res['answer'].items():
        
        sql = "SELECT answer FROM public.questionData WHERE id=(%s)"
        data = (str(keys),)
        cur.execute(sql,data)
        answer = cur.fetchone()
        answer = answer[0].replace(" ","")
        answerCheck = str(value).replace(" ","")
        
        if(answer.strip() == answerCheck.strip()):
            count = count+1
        

    sql = "INSERT INTO public.Result(examId,roll,marks) VALUES(%s,%s,%s)"
    data = (examIds[0],res["Roll"],count)
    cur.execute(sql,data)
    # code to remove logged student
    sql = "DELETE FROM public.activeStudents WHERE examId=(%s)"
    data = (examIds[0],)
    cur.execute(sql,data)
    
    db.commit()
    result=json.dumps("s")
    return(result)


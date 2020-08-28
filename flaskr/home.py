from flask import (Blueprint,g,Flask,redirect,render_template,request,url_for,flash)
from werkzeug.exceptions import abort
from flaskr.db import get_db
import json

bp = Blueprint('home',__name__)

@bp.route('/')
def index():
    sql = "SELECT Subject FROM public.EXAM WHERE status =(%s)"
    db = get_db()
    data = ('Active',)
    cur = db.cursor()   
    cur.execute(sql,data)
    result = cur.fetchall()
    
    return render_template('index.html',result=result)

@bp.route('/getSubject',methods=["GET","POST"])
def getSubject():
    sql = "SELECT Subject FROM public.EXAM WHERE status =(%s)"
    db = get_db()
    data = ('Active',)
    cur = db.cursor()   
    cur.execute(sql,data)
    result = cur.fetchall()
    result=json.dumps(result)
    return(result)

# Make a route to verify everything.i.e subject is active or not
#Roll number validation then redirect to paper.html page

@bp.route('/studentLogin',methods=["GET","POST"])
def studentLogin():
    res = request.get_json()
    Error = None
    print(res)
    sql = "SELECT * FROM public.EXAM WHERE status=(%s) and subject=(%s)"
    db = get_db()
    data = ('Active',res['Selectedsubject'])
    cur = db.cursor()
    cur.execute(sql,data)
    examResult = cur.fetchone()
    print(examResult)
    if(not examResult):
        Error = "Invalid subject"
        return(Error)
    sql = "SELECT roll FROM public.activestudents WHERE examId=(%s) and roll=(%s)"
    data = (examResult[0],res['rollNumber'])
    cur.execute(sql,data)
    result = cur.fetchone()
    if(not result):
        # not result means result is empty we can let the student proceed
        sql = "INSERT INTO public.activestudents(examId,roll,subject) VALUES(%s,%s,%s)"
        data = (examResult[0],res['rollNumber'],examResult[3])
        cur.execute(sql,data)
        db.commit()
    else:
        return("Given roll number is already taken by a user")
    return("ok")
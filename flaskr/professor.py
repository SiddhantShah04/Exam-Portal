from flask import (Blueprint,g,Flask,redirect,render_template,request,url_for,send_file,flash)
from werkzeug.exceptions import abort
import os
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




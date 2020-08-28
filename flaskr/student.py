from flask import (Blueprint,g,Flask,redirect,render_template,request,url_for,flash)
from werkzeug.exceptions import abort

bp = Blueprint('student',__name__,url_prefix='/student')

@bp.route("/home",methods=["POST"])
def home():
    Roll = request.form.get("Roll")
    Subject = request.form.get("Subject")
    print(Roll)
    return("Welcome")


  
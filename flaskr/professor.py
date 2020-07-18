from flask import (Blueprint,g,Flask,redirect,render_template,request,url_for,flash)
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('professor',__name__)

@bp.route("/professor")
def professor():
    db = get_db()
    return render_template("Professors.html")




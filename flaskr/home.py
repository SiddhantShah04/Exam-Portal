from flask import (Blueprint,g,Flask,redirect,render_template,request,url_for,flash)
from werkzeug.exceptions import abort

bp = Blueprint('home',__name__)

@bp.route('/')
def index():
    return render_template('index.html')

    
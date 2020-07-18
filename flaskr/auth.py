import functools
from flask import(Blueprint,flash,g,redirect,render_template,request,session,url_for)

from werkzeug.security import check_password_hash,generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register the user
@bp.route("/register",methods=["POST","GET"])
def register():
    if(request.method == "POST"):
        sql = "SELECT id from public.professor WHERE username=(%s);"
        error = None
        res = request.get_json()
        username = res["username"]
        password = res["password"]
        res = request.get_json()
        print(res["username"])
        db = get_db()
    
        data = (username,)
        cur = db.cursor()   
        cur.execute(sql,data)

        if(not username):
            error = "Email is required"
        elif(not password):
            error = "Password is required"
        elif(cur.fetchone() is not None):
            error = "User {} is already registered".format(username)

        if(error is None):
            sql = "INSERT INTO public.professor(username,password) VALUES(%s,%s);"
            data = (username,generate_password_hash(password))
            cur.execute(sql,data)
            db.commit()
            return("Congrats,your account has been created.")
        else:
            return(error)
        flash(error,'Registartion')
    print("s")
    return render_template("index.html")
    
# Logins in the user
@bp.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        cur = db.cursor()
        error = None
        sql = "SELECT * FROM public.professor WHERE username=(%s)"
        data = (username,)
        cur.execute(sql,data)
        user = cur.fetchone()
        
        if user is None:
            error = 'Incorrect Email.'
        elif not check_password_hash(str(user[2]),str(password)):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return(redirect(url_for("professor.professor")))
        flash(error,'login')

    return render_template("index.html")



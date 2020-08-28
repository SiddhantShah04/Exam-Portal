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

# Log out the user
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))
  
# Registers a function that runs before the view function, no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id') 
    if(user_id is None):
        g.user = None
    else:
        db = get_db()
        cur = db.cursor()
        sql = "SELECT * FROM public.professor WHERE id=(%s)"
        data = (user_id,) 
        cur.execute(sql,data) 
        g.user = cur.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


import psycopg2
import click
# g is a special object that is unique for each request. 
# It is used to store data that might be accessed by multiple functions during the request.
from flask import current_app,g
from flask.cli import with_appcontext

def get_db():
    if('db' not in g):
        g.db = psycopg2.connect(database="examportal", user = "postgres", password = "admin", 
        host = "127.0.0.1", port = "5432")
        return g.db

# Add the sql commands to the db.py
def init_db():
    db = get_db()
    cur = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        cur.execute(f.read().decode('utf8'))
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """clear the existing data and create new tables"""
    init_db()
    click.echo('initialized the databases.')

def close_db(e=None):
    db = g.pop('db',None)
    if(db is not None):
        db.close()

def init_app(app):
    #app.teardown_appcontext(close_db)
    # Add a command that can be called with flask command
    app.cli.add_command(init_db_command)
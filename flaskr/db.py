import psycopg2
import click
# g is a special object that is unique for each request. 
# It is used to store data that might be accessed by multiple functions during the request.
from flask import current_app,g
from flask.cli import with_appcontext

def get_db():
    
    g.db = psycopg2.connect(database="dfbekpi3f12dh6", user = "lenxkbuwhsvcjx", password = "279151d81303f68c9c9b96c27f871c7a984c23b9e6068f2f1fc2c239db37b573", 
        host = "ec2-107-20-167-241.compute-1.amazonaws.com",port="5432")
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
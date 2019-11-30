import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://axynzjdefwmyeo:e87f02858c1fbc56ea43154a07967f3d68c6e4ad7766daeee3eccc352380caa1@ec2-174-129-253-62.compute-1.amazonaws.com:5432/dcmaleb1aubmap"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()


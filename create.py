import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://lxwhjuhnkqxjzl:4b56351c072ef8f11a3b0ecde34fccf51b7e48d70986d4ecbdbf77ddc243cf7b@ec2-174-129-33-97.compute-1.amazonaws.com:5432/dik6pjhuaf1ne"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class tester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test1 = db.Column(db.String(80), unique=True)
    test2 = db.Column(db.String(120), unique=True)

    def __init__(self, test1, test2):
        self.test1 = test1
        self.test2 = test2

    def __repr__(self):
        return '<test %r>' % self.test1
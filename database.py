from flask import Flask,render_template,request,redirect,flash,make_response
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todolistdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='gfghbinojiuy'
db=SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Text)
    password = db.Column(db.Text)
    def __repr__(self):
        return f'user({self.username},{self.password})'

class Do(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    topic = db.Column(db.Text)
    date = db.Column(db.Text)
    time = db.Column(db.Text)
    description = db.Column(db.Text)
    date_of_register = db.Column(db.Text)
    user = db.Column(db.Text)
    def __repr__(self):
        return f'do({self.topic},{self.date}),{self.time}),{self.description}),{self.date_of_register},{self.user})'
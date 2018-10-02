from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '62b65bee7bcc1c12e978508825e15e91'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

class User(db.Model):
	username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	twitter = db.Column(db.String(30), nullable=False, unique=True)
	instagram = db.Column(db.String(30), nullable=False, unique=True)
	
	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.twitter}', {self.instagram})"

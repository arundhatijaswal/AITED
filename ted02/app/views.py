from flask import render_template
from app import app
from TestCodeThesis import genThesis
from forms import LoginForm
from flask import render_template, flash, redirect

@app.route('/')
@app.route('/index')
def index():
	thesis = 'Education'
	return render_template("index.html",
		topic = thesis)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	thesis = 'Education'
	form = LoginForm()
	return render_template('index.html',
		topic = thesis, 
		title = 'Sign In',
		form = form)

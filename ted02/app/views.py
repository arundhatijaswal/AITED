from flask import render_template
from app import app
from TestCodeThesis import gen_thesis
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
	if form.validate_on_submit():
		flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
		return redirect('/index')
	return render_template('index.html',
		topic = thesis, 
		title = 'Sign In',
		form = form)

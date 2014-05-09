import os
from flask import Flask, render_template, request
# from app import app
import version1
from forms import topicsForm 
from flask import Flask, redirect, url_for

app = Flask(__name__)
count = 0
app.secret_key = 'F34TF$($e34D'

def statement():
	title = ""
	thesis = ""
	try:
		title, thesis = version1.genThesis(topic)
		return title, thesis 
	except:
		return "no title", "no thesis"


@app.route('/', methods=['GET', 'POST'])
def index():
	form = topicsForm()
	if request.method == 'POST':
		topic = request.form['topics']
		if topic == 'Comedy': topic == 'Funny'
		elif topic == 'Transportation': topic == 'Cars'
		try:
			title, thesis = version1.genThesis(topic)
			return render_template('index.html', form=form, category=topic, thesis=thesis, title=title)
		except:
		# 	title, thesis = ""
		# if title == "" or thesis == "":
			 return redirect('', code=302)
		# else:
		
		# title or thesis == NoneType:
		# 	title, thesis = version1.genThesis(topic)
		# else:
	elif request.method == 'GET':
		# topic = request.form['topics']
		return render_template('index.html', form=form)


if __name__ == '__main__':
	# app.run(debug=True)
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
from flask import Flask, render_template, request
from app import app
import version1
from forms import topicsForm 

# app = Flask(__name__)

# app.secret_key = 'F34TF$($e34D'


@app.route('/', methods=['GET', 'POST'])
def index():
	form = topicsForm()
	if request.method == 'POST':
		topic = request.form['topics']
		title, thesis = version1.genThesis(topic)
		return render_template('index.html', form=form, category=topic, thesis=thesis, title=title)
	elif request.method == 'GET':
		# topic = request.form['topics']
		return render_template('index.html', form=form)


# if __name__ == '__main__':
# 	# app.run(debug=True)
# 	port = int(os.environ.get("PORT", 5000))
# 	app.run(debug=True, host='0.0.0.0', port=port)
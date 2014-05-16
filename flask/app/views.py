import os, random
from flask import Flask, render_template, request
# from app import app
import ScriptGen
from forms import topicsForm
from flask import Flask, redirect, url_for

app = Flask(__name__)
count = 0
app.secret_key = 'F34TF$($e34D'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = topicsForm()
    if request.method == 'POST':
        topic = request.form['topics']
        others = ['Arts', 'Movies', 'Music', 'People', 'Society', 'TV', 'News']

        if topic == 'Comedy': topic == 'Funny'
        elif topic == 'Transportation': topic == 'Cars'
        elif topic == 'Entertainment': topic == random.choice(others)
        elif topic == 'Wildcard': topic == 'Society'

        try:
            contents = ScriptGen.gen_thesis(topic)
            title = contents[0]
            thesis = contents[1]
            importance = contents[2]
            challenge = contents[3]
            solution = contents[4]
            impact = contents[5]

            while title == "" or thesis == "" or importance == "" or challenge == "" or solution == "" or impact == "":
                contents = ScriptGen.gen_thesis(topic)
                title = contents[0]
                thesis = contents[1]
                importance = contents[2]
                challenge = contents[3]
                solution = contents[4]
                impact = contents[5]
            return render_template('index.html', form=form, title=title, thesis=thesis, importance=importance, challenge=challenge, solution=solution, impact=impact)
        except:
            return redirect('', code=302)

    elif request.method == 'GET':
        return render_template('index.html', form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

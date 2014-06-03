import os, random, sys
from flask import Flask, render_template, request
# from app import app
import TED_Talk
# from forms import topicsForm
from flask import Flask, redirect, url_for

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.secret_key = 'F34TF$($e34D'


@app.route('/')
def form():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # form = topicsForm()
    # if request.method == 'POST':
    topic = ""
    topic = request.form['topics']
    print topic
    others = ['Arts', 'Movies', 'Music', 'People', 'Society', 'TV', 'News']

    if topic == 'Comedy': topic == 'Funny'
    elif topic == 'Transportation': topic == 'Cars'
    elif topic == 'Entertainment': topic == random.choice(others)
    elif topic == 'Wildcard': topic == 'Society'

    # run TED_Talk.py to generate the script
    open('talk.txt', 'w').close()
    contents = []

    TED_Talk.run(topic, debug=True)

    lines = open('talk.txt').read().splitlines()

    for i in lines:
        if i != '':
            contents.append(i)

    title = contents[0]
    thesis = contents[1]
    importance = contents[2]
    challenge = contents[3]
    solution = contents[4]
    impact = contents[5] 
    quote = contents[6]
    
    return render_template('results.html', 
                            topic = topic,
                            title = title, 
                            thesis = thesis, 
                            importance = importance,
                            challenge = challenge,
                            solution = solution, 
                            impact = impact,
                            quote = quote
                            )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)




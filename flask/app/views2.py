import os, random
from flask import Flask, render_template, request
# from app import app
import ScriptGen
import thesis2
# from forms import topicsForm
from flask import Flask, redirect, url_for

app = Flask(__name__)
app.secret_key = 'F34TF$($e34D'


@app.route('/')
def form():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # form = topicsForm()
    # if request.method == 'POST':
    topic = request.form['topics']
    print topic
    others = ['Arts', 'Movies', 'Music', 'People', 'Society', 'TV', 'News']

    if topic == 'Comedy': topic == 'Funny'
    elif topic == 'Transportation': topic == 'Cars'
    elif topic == 'Entertainment': topic == random.choice(others)
    elif topic == 'Wildcard': topic == 'Society'

    contents = []

    # title, thesis = thesis2.genThesis(topic)
    contents = ScriptGen.main(topic)
    title = contents[0]
    thesis = contents[1]
    importance = contents[2]
    challenge = contents[3]
    solution = contents[4]
    impact = contents[5]
    
    
    return render_template('results.html', 
                            topic = topic,
                            title = str(title), 
                            thesis = str(thesis), 
                            importance = str(importance),
                            challenge = str(challenge),
                            solution = str(solution), 
                            impact = str(impact)
                            )

    # try:
        

    #     while title == "" or thesis == "" or importance == "" or challenge == "" or solution == "" or impact == "":
    #         contents = ScriptGen.gen_thesis(topic)
    #         title = contents[0]
    #         thesis = contents[1]
    #         importance = contents[2]
    #         challenge = contents[3]
    #         solution = contents[4]
    #         impact = contents[5]
        
    # except:
    #     return redirect('/results/', code=302)

    # elif request.method == 'GET':
    #     return render_template('results.html', form=form)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password1'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    '''home page for surveys'''

    return render_template('home.html', survey = survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def collect_answers():
    choice = request.form['answer']
    responses.append(choice)

    return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:q_num>')
def show_question(q_num):

    if (len(responses) == len (survey.questions)):
        return redirect('/complete')

    if (len(responses) != q_num):
        flash(f'Invalid question: {q_num}.')
        return redirect(f'questions/{len(responses)}')

    question = survey.questions[q_num]
    return render_template('question.html', question = question, q_num = q_num)

@app.route('/complete')
def complete():
    return render_template('thank-you.html', responses = responses)


from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password1'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def home_page():
    '''home page for surveys'''

    return render_template('home.html', survey = survey)

@app.route("/begin", methods=["POST"])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def collect_answers():

    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:q_num>')
def show_question(q_num):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')

    if (len(responses) == len (survey.questions)):
        return redirect('/complete')

    if (len(responses) != q_num):
        flash(f'Invalid question: {q_num}.')
        return redirect(f'/questions/{len(responses)}')

    question = survey.questions[q_num]
    return render_template('question.html', question = question, q_num = q_num)

@app.route('/complete')
def complete():
    return render_template('thank-you.html')


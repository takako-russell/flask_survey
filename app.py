from flask import Flask,render_template,redirect,session,request,flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


RESPONSES_KEY = "reponses"

@app.route("/")
def choose_survey():
    """Choose a survey"""

    survey = surveys["satisfaction"]
    title = survey.title
    instruction = survey.instructions

    return render_template("start.html", title =title, instructions = instruction)


@app.route("/begin", methods=["POST"])
def start_newsurvey():
    """Clears all the answers in session"""
    #make the RESPONSES_KEY object empty in the session
    session[RESPONSES_KEY] = []

    return redirect("/question/0")


@app.route("/start")
def start_survey():
    """Shows instructions and starts a survey"""
   
    survey1 = surveys['satisfaction']
    instructions = survey1.instructions
    title = survey1.title

    return render_template("question.html", instructions, title)


@app.route("/answer", methods = ["POST"])
def store_answer():
    """Stores the choice in the session"""

    #Get the answer from input
    answer = request.form['answer']

    #Store the answer to the session
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    title = surveys["satisfaction"].title

    #redirect to complete page when all the questions are answered
    if len(responses) == len(surveys["satisfaction"].questions):

        return render_template("complete.html",title = title)
    else:
        return redirect(f"/question/{len(responses)}")



@app.route("/question/<int:qid>")
def show_questions(qid):
    """Shows a question"""

    #Get all the stored answers from the session
    answers = session.get(RESPONSES_KEY) 

    if len(answers) != qid:
    #Accessing the questions out of order
        flash("Invalid question Id")
        return redirect(f"/question/{qid}")
    
    if (answers is None):
    #Accessing the question too early
        return redirect("/")

    #Shows the question for the id
    survey = surveys["satisfaction"]
    nextq = survey.questions[qid]
    q_num = qid + 1
    return render_template("question.html",nextq = nextq, q_num =q_num)


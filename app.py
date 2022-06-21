from flask import Flask, request, render_template, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

KEY = "responses"

app = Flask (__name__)
app.config['SECRET_KEY'] = "oh-so-secret" 
# config needs to be right after the file naming
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# removes the redirection notification onscreen

debug = DebugToolbarExtension(app)
# passing in the app page

# root route
@app.route("/start")
def test_view_fun():
  '''Display survey instructions for user.'''
  title = satisfaction_survey.title
  instructions = satisfaction_survey.instructions

  return render_template("start.html", title=title, instructions =instructions)

# making a post request to clear any previous responses and using session method from flask to review/store user responses. 
@app.route("/begin", methods=["POST"])
def start_survey():
  '''Clear session responses. Redirect user to question 0.'''

  session[KEY] =[]

  return redirect("/questions/0")


# rendering a question per page by pulling an index and resp. question / choices

@app.route("/questions/<int:question_number>")
def load_questions(question_number):
  '''Render appropriate question amd choices for user to answer.'''

  responses= session.get(KEY)

  question = satisfaction_survey.questions[question_number]
  choices =  satisfaction_survey.questions[question_number].choices

  if len(responses) is None:
    return redirect ("/start")

  if len(responses) == len(satisfaction_survey.questions):
    return redirect("/complete")

  if len(responses) != question_number:
    flash(f"{question_number} is not a valid question. Redirecting you to the first unanswered question.")
    return redirect(f"/questions/{len(responses)}")
  
  return render_template("question.html", question = question, questions_number = question_number, choices = choices)


# Append user response to responses list and redirect to next question
@app.route("/answer", methods=["POST"])
def handle_responses():
  '''Grab form information and store the answers in the respones list. Direct user to next approporaite page based on response length.'''

  # grab user answer from the form
  answer = request.form["answer"]

  # add response to session
  responses = session[KEY]
  responses.append(answer)
  session[KEY] = responses

  if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
  else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def rennder_thankyou():
  '''Thank user for completing survey'''
  return render_template("thanks.html")


  




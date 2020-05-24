from flask import Flask, url_for
from flask import render_template
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from params import params
from params import days_of_week_dict
from params import goals
from params import tutors

app = Flask(__name__)
app.secret_key = 'my-super-secret-phrase-I-dont-tell-this-to-nobody'


class BookLessonForm(FlaskForm):
    name = StringField('Your name')
    phone = StringField('Your phone')
    submit = SubmitField()

@app.route("/")
def template_index():
    print(tutors)
    return render_template("index.html",
                           goals=goals,
                           tutors=tutors[:3],
                           **params)


@app.route("/goals/<goal>")
def template_goals(goal):
    goal_tutor_list = []
    for tutor in tutors:
        if goal in tutor['goals']:
            goal_tutor_list.append(tutor)
    return render_template("goal.html",
                           tutors=goal_tutor_list,
                           goals=goals,
                           curr_goal=goal,
                           **params)


@app.route("/profiles/<tutor_id>")
def template_profiles(tutor_id):
    curr_tutor = None
    for tutor in tutors:
        if tutor['id'] == int(tutor_id):
            curr_tutor = tutor
    return render_template("profile.html",
                           curr_tutor=curr_tutor,
                           curr_tutor_free=curr_tutor['free'],
                           goals=goals,
                           days_of_week_dict=days_of_week_dict,
                           **params)


@app.route("/request")
def template_request():
    return render_template("request.html",
                           **params)


@app.route("/request_done")
def template_request_done():
    return render_template("request_done.html",
                           **params)


@app.route("/booking/<tutor_id>/<day_of_week>/<time>/", methods=['GET','POST'])
def template_booking(tutor_id, day_of_week, time):
    curr_tutor = None
    for tutor in tutors:
        if tutor['id'] == int(tutor_id):
            curr_tutor = tutor

    book_form = BookLessonForm()
    return render_template("booking.html",
                           curr_tutor=curr_tutor,
                           goals=goals,
                           days_of_week_dict=days_of_week_dict,
                           day_of_week=day_of_week,
                           time=time,
                           book_form=book_form,
                           **params)


@app.route("/booking_done", methods=['GET'])
def template_book_done():
    return render_template("booking_done.html",
                           **params)



# if __name__ == '__main__':
#     app.run()

# with app.test_request_context():
#     print(url_for('template_departure', depart=123123))
#     # print(url_for('login'))
#     # print(url_for('login', next='/'))
#     # print(url_for('profile', username='John Doe'))
#     print("safasfasfasfasfasfsafsa")

app.run('0.0.0.0', 8000, debug=True)
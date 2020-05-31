from flask import Flask, url_for, request
from flask import render_template
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from params import params
from params import days_of_week_dict
from params import goals
from params import time_amount_dict

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'randomstring'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutors.db'
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Tutor(db.Model):
    __tablename__ = "tutors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(255*4), nullable=False)
    rating = db.Column(db.Float)
    picture = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    free = db.Column(db.JSON)
    goals = db.Column(db.JSON)

    booking = db.relationship("Booking", back_populates="tutor")


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    day_of_week = db.Column(db.String(10))
    time = db.Column(db.String(10))

    tutor = db.relationship("Tutor", back_populates="booking")
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutors.id'))


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(20))
    time_amount = db.Column(db.String(20)),
    goal = db.Column(db.String(20)),


######################################

def get_tutor_dict(tutor):
    return {
        'id': tutor.id,
        'name': tutor.name,
        'about': tutor.about,
        'rating': tutor.rating,
        'price': tutor.price,
        'picture': tutor.picture,
        'goals': tutor.goals,
        'free': tutor.free,
    }
######################################

class BookLessonForm(FlaskForm):
    name = StringField('Your name', [InputRequired()])
    phone = StringField('Your phone', [InputRequired()])
    submit = SubmitField()


class ApplySelectionForm(FlaskForm):
    goal = RadioField('Your goal', choices=[(k, v) for k, v in goals.items()], default='work', validators=[InputRequired()])
    time_amount = RadioField('Time you have', choices = [(k, v) for k, v in time_amount_dict.items()], default='key2', validators=[InputRequired()])
    name = StringField('Your name', [InputRequired()])
    phone = StringField('Your phone', [InputRequired()])
    submit = SubmitField('Request tutor search')

######################################

@app.route("/")
def template_index():
    tutors = []
    for tutor in db.session.query(Tutor).order_by(Tutor.rating.desc()).all():
        # print(tutor.id, tutor.name)
        tutors.append(get_tutor_dict(tutor))
    return render_template("index.html",
                           goals=goals,
                           tutors=tutors[:3],
                           **params)


@app.route("/goals/<goal>")
def template_goals(goal):
    tutors = []
    for tutor in db.session.query(Tutor).filter(Tutor.goals.contains(goal)).order_by(Tutor.rating.desc()).all():
        tutors.append(get_tutor_dict(tutor))

    return render_template("goal.html",
                           tutors=tutors,
                           goals=goals,
                           curr_goal=goal,
                           **params)


@app.route("/profiles/<tutor_id>")
def template_profiles(tutor_id):
    tutor_obj = db.session.query(Tutor).get(tutor_id)
    curr_tutor = get_tutor_dict(tutor_obj)

    return render_template("profile.html",
                           curr_tutor=curr_tutor,
                           curr_tutor_free=curr_tutor['free'],
                           goals=goals,
                           days_of_week_dict=days_of_week_dict,
                           **params)


@app.route("/request", methods=['GET','POST'])
def template_request():
    application_form = ApplySelectionForm()
    if request.method == 'GET':
        return render_template("request.html", application_form=application_form,
                           **params)
    else:
        appl = Application(
            student_name=application_form.name.data,
            phone_number=application_form.phone.data,
            time_amount=application_form.time_amount.data,
            goal=application_form.goal.data,
        )
        db.session.add(appl)
        db.session.commit()
        return render_template("request_done.html",
                               name=application_form.name.data,
                               phone=application_form.phone.data,
                               time_amount=time_amount_dict[application_form.time_amount.data],
                               goal=goals[application_form.goal.data],
                               **params)


@app.route("/booking/<tutor_id>/<day_of_week>/<time>/", methods=['GET','POST'])
def template_booking(tutor_id, day_of_week, time):
    tutor_obj = db.session.query(Tutor).get(tutor_id)
    curr_tutor = get_tutor_dict(tutor_obj)

    book_form = BookLessonForm()

    if request.method == "GET":
        return render_template("booking.html",
                               curr_tutor=curr_tutor,
                               goals=goals,
                               days_of_week_dict=days_of_week_dict,
                               tutor_id=curr_tutor['id'],
                               day_of_week=day_of_week,
                               time=time,
                               book_form=book_form,
                               **params)
    if request.method == "POST":
        booking = Booking(
            student_name=book_form.name.data,
            phone_number=book_form.phone.data,
            day_of_week=day_of_week,
            tutor_id=tutor_id,
            time=time,
        )
        db.session.add(booking)
        db.session.commit()
        return render_template("booking_done.html",
                               student_name=book_form.name.data,
                               phone_number=book_form.phone.data,
                               day_of_week=days_of_week_dict[day_of_week],
                               time=time,
                               **params)

# if __name__ == '__main__':
#     app.run()

# with app.test_request_context():
#     print(url_for('template_departure', depart=123123))
#     # print(url_for('login'))
#     # print(url_for('login', next='/')
#     # print(url_for('profile', username='John Doe'))
#     print("safasfasfasfasfasfsafsa")

# app.run('0.0.0.0', 8000, debug=True)
from flask import Flask, url_for, request
from flask import render_template
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from params import params
from params import days_of_week_dict
from params import goals
# from params import tutors

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




# import datetime
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.secret_key = 'randomstring'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
# class Product(db.Model):
#     __tablename__ = "products"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False, unique=True)
#     created_at = db.Column(db.DateTime, nullable=False)
#
# db.create_all()
#
# _products = []
# _products.append(Product(name="Бефстроганов классический", created_at=datetime.date(year=2000, month=4, day=3)))
# _products.append(Product(name="Грузди соленые", created_at=datetime.date(year=2000, month=2, day=10)))
# _products.append(Product(name="Гвозди жареные", created_at=datetime.date(year=2000, month=2, day=14)))
# _products.append(Product(name="Ряпушка по-карельски", created_at=datetime.date(year=2000, month=3, day=12)))
# _products.append(Product(name="Голубцы с перловкой и грибами", created_at=datetime.date(year=2000, month=4, day=2)))
# db.session.add_all(_products)
# Product.name
# db.session.commit()
#
# products_query = db.session.query(Product).order_by(Product.created_at)
# products = products_query.all()
# print("Получили", len(products), "продуктов")
# for product in products:
#     print("Продукт", product.name, "был создан", product.created_at)
#
# db.session.query(Product).get_or_404(13)
#
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#
#     mobile_phone = db.relationship("MobilePhone", uselist=False, back_populates="user")
#
#
# class MobilePhone(db.Model):
#     __tablename__ = 'mobile_phones'
#     id = db.Column(db.Integer, primary_key=True)
#     phone = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#
#     user = db.relationship("User", back_populates="mobile_phone")
#
# db.create_all()
# user = User()
# db.session.add(user)
# phone = MobilePhone(user=user, phone='1')
# print(phone.user)#<User (transient 4326580432)>
# print(user.mobile_phone)#<MobilePhone (transient 4343758992)>
# print(user.mobile_phone.user)#<MobilePhone (transient 4343758992)>
# db.session.commit()
# db.session.rollback()
# print(phone.user)#<User 2>
# print(user.mobile_phone)#<MobilePhone 2>


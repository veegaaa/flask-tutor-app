from flask import Flask, url_for
from flask import render_template
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import Tutor

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'randomstring'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutors.db'
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Fill the base
with open('data/tutors.json') as f:
    tutors_data = json.load(f)
    tutors_data_db_list = []
    for tutor_data in tutors_data:
        tutors_data_db_list.append(Tutor(
            id=int(tutor_data['id']),
            name=tutor_data['name'],
            about=tutor_data['about'],
            rating=float(tutor_data['rating']),
            picture = tutor_data['picture'],
            price=int(tutor_data['price']),
            goals=tutor_data['goals'],
            free=tutor_data['free'],
        ))

db.session.query(Tutor).delete()
db.session.add_all(tutors_data_db_list)
# db.session.rollback()
db.session.commit()

for t in db.session.query(Tutor).all():
    print(t.goals)

for t in db.session.query(Tutor).filter(Tutor.goals.contains('work')).all():
    print(t.goals)


from app import Booking
booking = Booking(
    student_name='Me',
    phone_number='+7909898',
    day_of_week='mon',
    tutor_id=123,
)
db.session.add(booking)
db.session.commit()

for t in db.session.query(Booking).all():
    print(t.tutor_id, t.id, t.time, t.student_name, t.day_of_week)

from app import Application
for t in db.session.query(Application).all():
    print(t, 1, t.student_name)

Application.__table__.drop(db.engine)
db.session.query("drop table applicationsasfasf")
db.session.commit()


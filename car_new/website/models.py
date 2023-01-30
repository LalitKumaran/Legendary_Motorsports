from . import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.String(150))
    city = db.Column(db.String(150))
    password = db.Column(db.String(150))
    user_type = db.Column(db.String(150))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_posted = db.Column(db.String, nullable=False)
    car_brand = db.Column(db.String(150))
    car_model = db.Column(db.String(150))
    fuel_type = db.Column(db.String(150))
    km_run = db.Column(db.Integer)
    make_year = db.Column(db.String(150))
    owner = db.Column(db.String(150))
    regno = db.Column(db.String(150))
    location = db.Column(db.String(150))
    price = db.Column(db.Integer)
    rendered_data1 = db.Column(db.Text, nullable=False)
    rendered_data2 = db.Column(db.Text, nullable=False)
    rendered_data3 = db.Column(db.Text, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))

import base64
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from . import db,mail
from .models import User, Car, Booking
import datetime
import matplotlib.pyplot as plt
from distutils.log import debug
from email import message
from sre_constants import SUCCESS
from flask_mail import Mail,Message


views = Blueprint('views', __name__)

curuser = 0

@views.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        from .models import User
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                flash('Logged in')
                global curuser
                curuser = user
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password')
        else:
            flash('User does not exist.')
    return render_template("login.html", user=curuser)

@views.route('/logout',methods=['GET','POST'])
def logout():
    global curuser
    curuser = 0
    flash('Logged out successfully.')
    return redirect(url_for('views.login'))

@views.route('/signup',methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('uname')
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        phone = request.form.get('phone')
        city = request.form.get('city')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        from .models import User
        user = User.query.filter_by(email=email).first()
        if user:
            flash('An account has already been created with this email.')
        elif password1 != password2:
            flash('Passwords don\'t match.')
        else:
            from . import db
            new_user = User(username=username, firstname=firstname, email=email,  password=password1, lastname=lastname, phone=phone, city=city, user_type="test")
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up.')
            return redirect(url_for('views.login'))

    return render_template("signup.html", user=curuser)

@views.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")

@views.route('/home', methods=['GET', 'POST'])
def home():
    if curuser != 0:
        car = Car.query.all()
        return render_template("home.html", user=curuser, car=car)
    else:
        return redirect(url_for('views.login')) 

@views.route('/car/<int:car_id>', methods=['GET', 'POST'])
def car(car_id):
    if curuser != 0:
        car = Car.query.get(car_id)
        book = Booking.query.all()
        userr = User.query.all()
        seller = User.query.filter_by(id=car.user_id).first()
        return render_template("car.html",car=car,user=curuser,book=book,userr = userr,seller=seller)
    else:
        return redirect(url_for('views.login'))

@views.route('/book/<int:car_id>', methods=['GET', 'POST'])
def book(car_id):
    if curuser != 0:
        car = Car.query.get(car_id)
        uder = User.query.filter_by(id=car.user_id).first()
        subject="Car Booking"
        msg="Your car has been booked by " + str(curuser.firstname) + " " + str(curuser.lastname) 
        message=Message(subject,sender="kiruthickkumark.20cse@kongu.edu",recipients=[uder.email])
        message.body=msg
        mail.send(message)
        new_book = Booking(car_id=car_id, user_id=curuser.id)
        db.session.add(new_book)
        db.session.commit()
        flash('Car Booked')
        return redirect(url_for('views.car',car_id=car_id))
    else:
        return redirect(url_for('views.login'))

@views.route('/removebook/<int:book_id>', methods=['GET', 'POST'])
def removebook(book_id):
    if curuser != 0:
        book = Booking.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        flash("Booking Removed")
        return redirect(url_for('views.view_profile',user_id=curuser.id))
    else:
        return redirect(url_for('views.login'))
    
@views.route('/removecar/<int:car_id>', methods=['GET', 'POST'])
def removecar(car_id):
    if curuser != 0:
        car = Car.query.get(car_id)
        db.session.delete(car)
        db.session.commit()
        flash("Car Removed")
        return redirect(url_for('views.view_profile',user_id=curuser.id))
    else:
        return redirect(url_for('views.login'))

def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

@views.route('/sell',methods=['GET', 'POST'])
def sell():
    if curuser != 0:
        car = Car.query.all()
        use = curuser.id
        if request.method == 'POST':
            date = str(datetime.date.today())
            brand = request.form.get('brand')
            model = request.form.get('model')
            variant = request.form.get('variant')
            regno = request.form.get('regno')
            myear = request.form.get('myear')
            km = request.form.get('km')
            price = request.form.get('price')
            location = request.form.get('location')
            owner = request.form.get('owner')
            file1 = request.files['image1']
            data1 = file1.read()
            render_file1 = render_picture(data1)
            file2 = request.files['image2']
            data2 = file2.read()
            render_file2 = render_picture(data2)
            file3 = request.files['image3']
            data3 = file3.read()
            render_file3 = render_picture(data3)
            new_car = Car(user_id=use, date_posted=date,car_brand = brand, car_model = model, fuel_type = variant, km_run = km, make_year = myear, owner = owner, location = location, price = price, rendered_data1 = render_file1, rendered_data2 = render_file2, rendered_data3 = render_file3, regno=regno)
            db.session.add(new_car)
            db.session.commit()
            flash('Successfully put on sale.')
            return redirect(url_for('views.home')) 

        return render_template("sell.html", user=curuser, car=car)
    else:
        return redirect(url_for('views.login'))

@views.route('/profile/<int:user_id>',methods=['GET', 'POST'])
def view_profile(user_id):
    if curuser != 0:
        use = User.query.get(curuser.id)
        name1 = use.firstname
        last1 = use.lastname
        emai = use.email
        phone = use.phone
        city = use.city
        usee = User.query.all()
        car = Car.query.all()
        book = Booking.query.all()
        return render_template("profile.html",user=curuser,name1=name1,last1=last1,emai=emai,phone=phone,city=city,car=car,book=book,usee=usee)
    else:
        return redirect(url_for('views.login'))

@views.route('/compare',methods=['GET', 'POST'])
def compare():
    car = Car.query.all()
    if request.method == 'POST':
        car1 = request.form.get('car1')
        car2 = request.form.get('car2')
        return redirect(url_for('views.compare_cars',car_id_1=car1,car_id_2=car2))
    return render_template("compare.html",user=curuser,car=car)

@views.route('compare/<int:car_id_1>/<int:car_id_2>',methods=['GET', 'POST'])
def compare_cars(car_id_1,car_id_2):
    car1 = Car.query.get(car_id_1)
    car2 = Car.query.get(car_id_2)

    return render_template("comparecars.html",user=curuser,car1=car1,car2=car2)


from flask import Flask , session 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import secrets
from PIL import Image
import os
from flask import render_template, url_for, flash, redirect, request
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
    login_required,
)
from datetime import datetime
from flask_login import UserMixin

from tokenize import String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    EqualTo,
    ValidationError,
)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


with app.app_context():
    db.create_all()



courses = [
    {
        "name": "Python",
        "icon": "python.svg",
        "description": "Python is a general-purpose programming language that’s powerful yet easy to read, making it a great first language to learn.",
        "price" : "300",
    },
    {
        "name": "Data_Analysis",
        "icon": "analysis.png",
        "description": "Data analysis is the practice of working with data to glean useful information, which can then be used to make informed decisions.",
        "price" : "150",

    },
    {
        "name": "Machine_Learning",
        "icon": "machine-learning.png",
        "description": "(ML) is the process of using mathematical models of data to help a computer learn without direct instruction. It’s considered a subset of artificial intelligence (AI)",
        "price" : "100",

    },
    {
        "name": "Web_Design",
        "icon": "web.png",
        "description": "Web design is the art of planning and arranging content on a website so that it can be shared and accessed online with the world",
        "price" : "200",
    },
    {
        "name": "Blockchain",
        "icon": "blockchain.png",
        "description": "Blockchain is a type of ledger technology that stores and records data.",
        "price" : "350",
    },
    {
        "name": "Algorithm",
        "icon": "idea.png",
        "description": "is a set of commands that must be followed for a computer to perform calculations or other problem-solving operations.",
        "price" : "200",
    },
]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def init(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# Ensure this runs once, e.g., when you first set up the application
with app.app_context():
    db.create_all()

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {e}', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['email'] = user.email
            session['name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))





class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(20), nullable=False, default="default_icon.jpg")

    def __repr__(self):
        return f"Course('{self.title}')"


@app.route("/")
@app.route("/home")
def home():
    name = session.get('name')

    return render_template("home.html",  courses=courses)


@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/add_to_cart")
def add_to_cart():
    return render_template("add_to_cart.html")


@app.route("/course/<string:course_name>")
def course_detail(course_name):
    course = Course.query.filter_by(title=course_name).first_or_404()
    return render_template('course_detail.html', course=course)


@app.route('/course/blockchain')
def blockchain_course():
    return render_template('blockchain_course.html')

@app.route('/course/python')
def python_course():
    return render_template('Python_course.html')

@app.route('/course/data_analysis_course')
def Data_Analysis():
    return render_template('Data_Analysis.html')

@app.route('/machine_learning')
def machine_learning():
    return render_template('machine_learning.html')

@app.route('/web_design_course')
def web_design():
    return render_template ("web_design.html")

@app.route('/algorithms')
def algorithms ():
    return render_template ("algorithms.html")

if __name__ == "__main__":
    app.run(debug=True)

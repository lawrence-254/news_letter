from flask import Blueprint, render_template, url_for, flash, redirect
from newsLetter.forms import RegistrationForm, LoginForm
from newsLetter.models import User, Post, Reaction, posts
from newsLetter import app


routes = Blueprint('routes', __name__)


@routes.route("/")
@routes.route("/home/")
def home():
    return render_template('home.html', posts=posts, title='Home')


@routes.route("/about/")
def about():
    return render_template('about.html', title='About')


@routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"{form.username.data}'s Account created successfully", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@routes.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"welcome back {form.email.data}", 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

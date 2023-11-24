from flask import render_template, url_for, flash, redirect
from newsLetter import app, db, bcrypt
from newsLetter.forms import RegistrationForm, LoginForm
from newsLetter.models.models import User, Post, Reaction, posts


@app.route("/")
@app.route("/home/")
def home():
    return render_template('home.html', posts=posts, title='Home')


@app.route("/about/")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    '''generates a hashed password'''
    hashed_password = bcrypt.generate_password_hash(
        form.password.data).decode('utf-8')
    user_query = User(
        username=form.username.data,
        email=form.email.data,
        password=hashed_password)
    db.session.add(user_query)
    db.session.commit()
    if form.validate_on_submit():
        flash(f"Success, please login", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"welcome back {form.email.data}", 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

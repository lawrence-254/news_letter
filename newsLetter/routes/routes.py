import os
import secrets
from flask import render_template, request, url_for, flash, redirect
from newsLetter import app, db, crypt
from newsLetter.forms import RegistrationForm, LoginForm, UpdateDetailsForm, PostForm
from newsLetter.models.models import User, Post, Reaction
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home/")
def home():
    return render_template('home.html', title='Home')


@app.route("/about/")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate hashed password
        pwd = form.password.data
        hashed_password = crypt.generate_password_hash(pwd).decode('utf-8')
        # Create a new user with the hashed password
        user_query = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        # Add the user to the database and commit the changes
        db.session.add(user_query)
        db.session.commit()
        flash(f"Success, please login", 'success')
        return redirect(url_for('login'))
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and crypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"welcome back", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Login not successful, please check password and email", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(input_picture):
    rand = secrets.token_hex(4)
    _, file_extension = os.path.splitext(input_picture.filename)
    pic_filename = rand + file_extension
    pic_path = os.path.join(app.root_path, 'static/avi', pic_filename)
    input_picture.save(pic_path)
    return pic_filename

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateDetailsForm()
    if form.validate_on_submit():
        if form.picture.data:
            avi_image = save_picture(form.picture.data)
            current_user.user_avi =  avi_image
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account details update success', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avi_image = url_for('static', filename='avi/'+ current_user.user_avi)
    return render_template(
        'account.html',
        title='Account',
        avi_image=avi_image,
        form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content= form.content.data)
        flash('post created successfully')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)

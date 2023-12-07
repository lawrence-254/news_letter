from flask import render_template, request, url_for, flash, redirect, abort, Blueprint
from newsLetter import db, crypt
from flask_login import login_user, current_user, logout_user, login_required
from newsLetter.users.forms import RegistrationForm, LoginForm, UpdateDetailsForm, ResetPasswordForm, ResetRequestForm
from newsLetter.models.models import User, Post, Reaction
from newsLetter.users.utilities import send_to_reset_email, save_picture, allowed_file, get_paginated_reactions



users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
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


@users.route("/login", methods=['GET', 'POST'])
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

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    Posts= Post.query.all()
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
        form=form,
        posts=Posts)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_to_reset_email(user)
        flash('Check your email for the reset token which is valid for 1 hour', 'warning')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_request_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Your token is invalid or expired', 'danger')
        return redirect(url_for('login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Generate hashed password
        pwd = form.password.data
        hashed_password = crypt.generate_password_hash(pwd).decode('utf-8')
        user.password = hashed_password
        # Add the user to the database and commit the changes
        db.session.commit()
        flash(f"password update Success, please login", 'success')
        return redirect(url_for('login'))
    return render_template('reset_request_token.html', title='Reset Password', form=form)
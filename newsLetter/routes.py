import os
import secrets
from werkzeug.utils import secure_filename
from flask import render_template, request, url_for, flash, redirect, abort
from newsLetter import app, db, crypt, mail
from newsLetter.forms import RegistrationForm, ReactionForm, LoginForm, UpdateDetailsForm, PostForm, ResetPasswordForm, ResetRequestForm
from newsLetter.models.models import User, Post, Reaction
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


# '''Home route section'''
@app.route("/")
@app.route("/home/")
def home():
    '''Home route section'''
    page = request.args.get('page', 1, type=int)
    posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('home.html', posts=posts, title='Home')
# '''end of home route'''

# '''about route'''
@app.route("/about/")
def about():
    '''about route'''
    return render_template('about.html', title='About')


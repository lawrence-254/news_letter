'''A file containing form classes'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from newsLetter.models.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    '''
    A python class that outlines a registration form defining the details
    and parameters
    '''
    username = StringField('User Name', validators=[
                           DataRequired(), Length(min=6, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        '''checks for username duplication'''
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User name exist, please choose another one')
    def validate_email(self, email):
        '''checks for email duplication'''
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email exist, please check your email')


class LoginForm(FlaskForm):
    '''
    A python class that outlines a login form defining the details
    and parameters
    '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateDetailsForm(FlaskForm):
    '''
    A python class that outlines a update details form defining the details
    and parameters
    '''
    username = StringField('User Name', validators=[
                           DataRequired(), Length(min=6, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')
    def validate_username(self, username):
        '''checks for username duplication'''
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('User name exist, please choose another one')

    def validate_email(self, email):
        '''checks for email duplication'''
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email exist, please check your email')
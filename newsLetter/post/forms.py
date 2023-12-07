from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    '''a form used to make/create posts'''
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    content_image = FileField('Content Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')


class ReactionForm(FlaskForm):
    '''Form to record reaction i.e  comments'''
    comment = TextAreaField('Comment')
    like = BooleanField('Like')
    flag = BooleanField('Flag')
    submit = SubmitField('Submit')


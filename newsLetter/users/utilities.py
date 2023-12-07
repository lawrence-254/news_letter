import os
import secrets
from flask import url_for
from flask_mail import Message
from newsLetter import app, mail

def save_picture(input_picture):
    rand = secrets.token_hex(4)
    _, file_extension = os.path.splitext(input_picture.filename)
    pic_filename = rand + file_extension
    pic_path = os.path.join(app.root_path, 'static/avi', pic_filename)
    input_picture.save(pic_path)
    return pic_filename

UPLOAD_FOLDER = 'static/content_images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_paginated_reactions(page=1, per_page=10):
    '''retrieves reaction data'''
    return Reaction.query.paginate(page=page, per_page=per_page, error_out=False)


def send_to_reset_email(user):
    try:
        token = user.get_reset_token()
    except Exception as e:
        print(f"Error generating reset token: {e}")
        return "Error generating reset token"
    msg = Message(
        'Password reset request successful',
        sender='newsletter@mail.com',
        recipients=[user.email])
    msg.body = f'''
visit this link {url_for('reset_request_token', token=token, _external=True)} to reset tour password.

Ignore  this if you did not request a password change
'''
    try:
        mail.send(msg)
        return "Password reset email sent successfully"
    except Exception as e:
        print(f"Error sending reset email: {e}")
        return "Error sending reset email"

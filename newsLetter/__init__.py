from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from newsLetter.config import Config



app = Flask(__name__)

app.config.from_object(Config)
'''sql db imports'''
'''mysql config for deployment'''

db = SQLAlchemy(app)
'''end of sql configs'''
'''hashing'''
crypt = Bcrypt(app)
'''login manager'''
login_manager = LoginManager(app)
login_manager.login_view ='users.login'
login_manager.login_message_category ='danger'



mail = Mail(app)

''' import route '''
from newsLetter.users.routes import users
from newsLetter.post.routes import posts
from newsLetter.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
'''sql tables'''
with app.app_context():
    # Create all tables
    db.create_all()
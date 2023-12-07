from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


app = Flask(__name__)
'''secret key'''
app.config['SECRET_KEY'] = 'f43e0ff5e0ad8b9594af298c550b92ca'

'''sql db imports'''
'''mysql config for deployment'''
databaseLink = 'mysql+mysqlconnector://root@localhost/news_letter'
app.config['SQLALCHEMY_DATABASE_URI'] = databaseLink
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
'''end of sql configs'''
'''hashing'''
crypt = Bcrypt(app)
'''login manager'''
login_manager = LoginManager(app)
login_manager.login_view ='login'
login_manager.login_message_category ='danger'

'''mail configs'''
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')


mail = Mail(app)

''' import route '''
from newsLetter.routes import routes
'''sql tables'''
with app.app_context():
    # Create all tables
    db.create_all()
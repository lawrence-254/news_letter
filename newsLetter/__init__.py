from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from newsLetter.config import Config




'''sql db imports'''
'''mysql config for deployment'''

db = SQLAlchemy()
'''end of sql configs'''
'''hashing'''
crypt = Bcrypt()
'''login manager'''
login_manager = LoginManager()
login_manager.login_view ='users.login'
login_manager.login_message_category ='danger'



mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    crypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ''' import route '''
    from newsLetter.users.routes import users
    from newsLetter.post.routes import posts
    from newsLetter.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    return app
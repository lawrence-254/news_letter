from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from newsLetter.routes import routes

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
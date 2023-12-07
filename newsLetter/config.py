import os
class Config:
    # postgressdblink = postgres://news_letter_user:QbOCIWZC3na9byfU8uIIs79FlUQGciou@dpg-closdvhoh6hc73bn2ps0-a/news_letter
    # databaseLink = 'mysql+mysqlconnector://root@localhost/news_letter'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'f43e0ff5e0ad8b9594af298c550b92ca'
    # '''secret key'''
    # SECRET_KEY = os.environ.get('SECRET_KEY')

    # '''db'''
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''mail configs'''
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # postgres://news_letter_user:QbOCIWZC3na9byfU8uIIs79FlUQGciou@dpg-closdvhoh6hc73bn2ps0-a.oregon-postgres.render.com/news_letter
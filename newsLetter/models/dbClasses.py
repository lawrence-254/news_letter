'''A file containing different database classes'''
from datetime import datetime
from . import db

# dummy data
posts = [
    {
        'author': 'peter griffin',
        'title': 'peter copter',
        'content': 'flying',
        'date_posted': 'january 15, 2020'
    },
    {
        'author': 'stew griffin',
        'title': 'the duce',
        'content': 'victory shall be mine',
        'date_posted': 'february 14, 2020'
    }
]
# end of dummy data

# sql class models
# class user


class User(db.Model):
    '''A class containing user details  and structure'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    user_avi = db.Column(db.String(25), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    posts = db.relationship('Post', backref='author', lazy=True)
    reaction = db.relationship('Reaction', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_avi}')"

# end of class user
# class posts


class Post(db.Model):
    '''A class containing post details and structure'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    content_image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# end of class posts
# class relationship


class Reaction(db.Model):
    '''A class containing reaction details and structure'''
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    comment = db.Column(db.Text)
    like = db.Column(db.String)
    flag = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f"Reaction('{self.like}', '{self.date_posted}')"

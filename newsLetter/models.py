'''A file containing different database classes'''
from itsdangerous import TimedSerializer
from datetime import datetime
from newsLetter import db, login_manager, app
from flask_login import UserMixin


'''auxiliary function to load user'''
@login_manager.user_loader
def load_user(user_id):
    id_user = int(user_id)
    return User.query.get(id_user)

'''sql class models'''
'''class user'''
class User(db.Model, UserMixin):
    '''A class containing user details  and structure'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    user_avi = db.Column(db.String(25), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)


    posts = db.relationship('Post', backref='author', lazy=True)
    reaction = db.relationship('Reaction', backref='author', lazy=True)

    def get_reset_token(self, expires_in_sec=3600):
        s = TimedSerializer(app.config['SECRET_KEY'], expires_in_sec)
        token_bytes = s.dumps({'user_id': self.id})
        return token_bytes.decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = TimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            user_id = data['user_id']
            return User.query.get(user_id)
        except Exception as e:
            return None
        return User.query.get()


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
    content_image = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reaction = db.relationship('Reaction', backref='post', lazy=True)


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
    like = db.Column(db.Boolean, default=False)
    flag = db.Column(db.Boolean, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Reaction('{self.like}', '{self.date_posted}')"

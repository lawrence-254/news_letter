from newsLetter.models import User, Post, Reaction, posts
from newsLetter import app, db
from newsLetter.routes import routes

'''A python file that is used to run the news letter web app'''
app.register_blueprint(routes)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

from newsLetter.models.models import User, Post, Reaction, posts
from newsLetter import app, db
from newsLetter.routes import routes

'''A python file that is used to run the news letter web app'''


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

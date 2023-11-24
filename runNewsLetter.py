from newsLetter.models.models import User, Post, Reaction
from newsLetter import app, db
from newsLetter.routes import routes

'''A python file that is used to run the news letter web app'''

'''create a db'''
# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

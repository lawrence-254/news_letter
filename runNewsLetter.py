from newsLetter.models import User, Post, Reaction
from newsLetter import create_app


'''A python file that is used to run the news letter web app'''

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, url_for
app = Flask(__name__)

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


@app.route("/")
@app.route("/home/")
def home():
    return render_template('home.html', posts=posts, title='Home')


@app.route("/about/")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)

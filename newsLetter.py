from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# secret key
app.config['SECRET_KEY'] = 'f43e0ff5e0ad8b9594af298c550b92ca'
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite///'

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


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"{form.username.data}'s Account created successfully", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"welcome back {form.email.data}", 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)

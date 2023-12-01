import os
import secrets
from werkzeug.utils import secure_filename
from flask import render_template, request, url_for, flash, redirect, abort
from newsLetter import app, db, crypt
from newsLetter.forms import RegistrationForm, ReactionForm, LoginForm, UpdateDetailsForm, PostForm
from newsLetter.models.models import User, Post, Reaction
from flask_login import login_user, current_user, logout_user, login_required


# '''Home route section'''
@app.route("/")
@app.route("/home/")
def home():
    '''Home route section'''
    Posts= Post.query.all()
    return render_template('home.html', posts=Posts, title='Home')
# '''end of home route'''

# '''about route'''
@app.route("/about/")
def about():
    '''about route'''
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate hashed password
        pwd = form.password.data
        hashed_password = crypt.generate_password_hash(pwd).decode('utf-8')
        # Create a new user with the hashed password
        user_query = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        # Add the user to the database and commit the changes
        db.session.add(user_query)
        db.session.commit()
        flash(f"Success, please login", 'success')
        return redirect(url_for('login'))
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and crypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"welcome back", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"Login not successful, please check password and email", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(input_picture):
    rand = secrets.token_hex(4)
    _, file_extension = os.path.splitext(input_picture.filename)
    pic_filename = rand + file_extension
    pic_path = os.path.join(app.root_path, 'static/avi', pic_filename)
    input_picture.save(pic_path)
    return pic_filename

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    Posts= Post.query.all()
    form = UpdateDetailsForm()
    if form.validate_on_submit():
        if form.picture.data:
            avi_image = save_picture(form.picture.data)
            current_user.user_avi =  avi_image
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account details update success', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avi_image = url_for('static', filename='avi/'+ current_user.user_avi)
    return render_template(
        'account.html',
        title='Account',
        avi_image=avi_image,
        form=form,
        posts=Posts)

UPLOAD_FOLDER = 'static/content_images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content= form.content.data, author=current_user)
        if form.content_image.data:
            image_file = form.content_image.data
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.root_path, UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                post.content_image = f'content_images/{filename}'
        db.session.add(post)
        db.session.commit()
        flash('post created successfully')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    reaction_form = ReactionForm()
    reactions = Reaction.query.filter_by(post_id=post.id).paginate(page=request.args.get('page', 1, type=int), per_page=5)
    total_likes = Reaction.query.filter_by(post_id=post.id, like=True).count()
    total_flags = Reaction.query.filter_by(post_id=post.id, flag=True).count()
    return render_template('post.html', title=post.title, post=post, reaction_form=reaction_form, reactions=reactions, total_likes=total_likes, total_flags=total_flags)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.content_image = form.content_image.data

        if form.content_image.data:
            image_file = form.content_image.data
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.root_path, UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                post.content_image = os.path.join('content_images', filename)

        db.session.commit()
        flash(f'Post Update Success', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        'create_post.html',
        title='Update Your Post',
        form=form,
        legend='Update Your Post')

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post deleted!', 'info')
    return redirect(url_for('home'))

def get_paginated_reactions(page=1, per_page=10):
    '''retrieves reaction data'''
    return Reaction.query.paginate(page=page, per_page=per_page, error_out=False)

@app.route('/post/<int:post_id>/post_reaction', methods=['GET', 'POST'])
@login_required
def post_reaction(post_id):
    '''post id'''
    post = Post.query.get_or_404(post_id)
    reaction_form = ReactionForm()
    reactions = get_paginated_reactions(page=request.args.get('page', 1))
    '''retrieve form values'''
    current_form_values = Reaction.query.filter_by(
        author=current_user,
        post_id=post_id
        ).order_by(Reaction.id.desc()).first()
    '''check for like flag population'''
    if current_form_values:
        reaction_form.like.default = current_form_values.like
        reaction_form.flag.default = current_form_values.flag
        reaction_form.process()
    '''validate incoming values'''
    if reaction_form.validate_on_submit():
        reaction = Reaction(
            comment=reaction_form.comment.data,
            like=reaction_form.like.data,
            flag=reaction_form.flag.data,
            author=current_user,
            post_id=post_id
            )
        db.session.add(reaction)
        db.session.commit()
        flash('Reacted to post successfully', 'success')
        return redirect(url_for('post', post_id=post.id))
    print(f"post: {post}")
    print(f"reaction_form: {reaction_form}")
    return render_template('post.html', post=post, reactions=reactions, reaction_form=reaction_form)


from flask import render_template, request, url_for, flash, redirect, abort, Blueprint
from flask_login import current_user, login_required
from newsLetter import db
from newsLetter.models import Post, Reaction
from newsLetter.post.forms import ReactionForm, PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
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


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    reaction_form = ReactionForm()
    reactions = Reaction.query.filter_by(post_id=post.id).paginate(page=request.args.get('page', 1, type=int), per_page=5)
    total_likes = Reaction.query.filter_by(post_id=post.id, like=True).count()
    total_flags = Reaction.query.filter_by(post_id=post.id, flag=True).count()
    return render_template('post.html', title=post.title, post=post, reaction_form=reaction_form, reactions=reactions, total_likes=total_likes, total_flags=total_flags)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post deleted!', 'info')
    return redirect(url_for('home'))


@posts.route('/post/<int:post_id>/post_reaction', methods=['GET', 'POST'])
@login_required
def post_reaction(post_id):
    '''post id'''
    post = Post.query.filter_by(id=post_id).first_or_404()
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




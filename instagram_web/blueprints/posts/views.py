import os
from peewee import IntegrityError

from models.post import Post
from instagram_web.blueprints.posts.forms import PostForm

from app import (render_template, flash, redirect, url_for, request, 					session, escape, Blueprint, abort,
				login_user, logout_user, login_required, current_user, LoginManager)

web_dir = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), 'instagram_web')
posts_blueprint = Blueprint('posts',
							__name__,
							template_folder='templates/posts')

@posts_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form =PostForm()
	if form.validate() and request.method == 'POST':
		post = Post(title=form.content.data, content=form.content.data, author=current_user)
		post.save()
		flash('New post created', 'success')
		return redirect(url_for('users.index'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts_blueprint.route('/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@posts_blueprint.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.save(form.title.data, form.content.data)
		flash('Post updated!', 'info')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form)

@posts_blueprint.route("/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	# How to execute the delete command???
	flash('Post has been deleted!', 'info')
	return redirect(url_for('home'))
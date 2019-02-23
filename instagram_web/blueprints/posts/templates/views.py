from peewee import IntegrityError

from models.post import Post
# from instagram_web.blueprints.posts.forms import PostForm
from instagram_web.blueprints.posts.forms import PostForm
from app import (app,
				 Flask, render_template, flash, redirect, url_for, request,
				 login_user, logout_user, login_required, current_user, LoginManager,
				 Image,
				 CsrfProtect, Blueprint, session, escape, CsrfProtect, os)

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

@posts_blueprint.route('/', methods=["GET", 'POST'])
def index():
	pass

@posts_blueprint.route('/', methods=['GET', 'POST'])
def create():
	pass

@posts_blueprint.route('/<username>', methods=["GET"])
def show(username):
	pass

@posts_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
	pass
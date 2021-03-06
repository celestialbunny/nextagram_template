from werkzeug.security import check_password_hash, generate_password_hash
import secrets, os
from PIL import Image
from peewee import IntegrityError

from models.user import User
from instagram_web.blueprints.users.forms import (RegistrationForm, LoginForm, UpdateDetailsForm)
from util.s3_helper import upload_file_to_s3

from app import (app, render_template, flash, redirect, url_for, request, 					session, escape, Blueprint,
				login_user, logout_user, login_required, current_user, LoginManager)

web_dir = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), 'instagram_web')
users_blueprint = Blueprint('users',
							__name__,
							template_folder='templates/users')

def redirect_if_logged_in():
	if current_user.is_authenticated:
		flash("You have already been logged in", "warning")
		return redirect(url_for('users.index'))

@users_blueprint.route('/', methods=["GET", 'POST'])
def index():
	breakpoint()
	return render_template('index.html')

def save_picture(form_picture):
	# Generate random tokens to prevent filename from being similar
	# split the filename and ext so that we can further process the ext
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)


	# profile pic is often small and no reason to take up too much bandwidth
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	# return picture filename
	return picture_fn

@users_blueprint.route('/update', methods=['POST', 'GET'])
@login_required
def update():
	form = UpdateDetailsForm()
	if request.method == 'POST' and form.validate():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		# How to update the details??????
		# current_user.save(form.username.data, form.email.data)
		flash("Update successful", "success")
		return redirect(url_for('users.index'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('update.html', image_file=image_file, form=form)

@users_blueprint.route("/register", methods=['GET', 'POST'])
def register():
	redirect_if_logged_in()
	form = RegistrationForm()
	if request.method == 'POST' and form.validate():
		try:
			new_user = User(
				username=form.data['username'],
				email=form.data['email'],
				password=generate_password_hash(form.data['password'])
			)
			new_user.save()
			flash("Thanks for registering", "success")
			return redirect(url_for('users.login'))
		except IntegrityError:
			# new_user.validate_username(form.data['username'])
			# new_user.validate_email(form.data['email'])
			# Still need to get the 2 lines above to work
			flash('Duplication of either username or email', 'warning')
	return render_template('register.html', register_form=form)


@users_blueprint.route("/login", methods=['GET', 'POST'])
def login():
	redirect_if_logged_in()
	form = LoginForm()
	if request.method == 'POST':
		if form.validate():
			user = User.get_or_none(User.email == form.data['email'])
			if user and check_password_hash(user.password, form.data['password']):
				# login_user(user, remember=form.remember.data)
				login_user(user)
				next_page = request.args.get('next')
				flash("You've been logged in!", "success")
				if next_page:
					return redirect(url_for(next_page))
				else:
					return redirect(url_for('users.index', current_user=user))
			else:
				flash("Login unsuccessful, Please check email and password", "danger")
	return render_template('login.html', login_form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out!", "success")
	return redirect(url_for('users.login'))

@users_blueprint.route('/')
def upload():
	file = request.file["user_file"]
	output = upload_file_to_s3(file, app.config['celestialbunny-nextagram'])
	return render_template('users/edit_profile_pic.html')

@users_blueprint.route('/', methods=['POST'])
def upload_file():
	return 'haha'
	# refer to util/<random name: such as s3_helper.py> to help s3 account posting
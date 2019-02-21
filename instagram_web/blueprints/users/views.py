from flask import Blueprint, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CsrfProtect
import os

from models.user import User
from instagram_web.blueprints.users.forms import RegistrationForm, LoginForm, UpdateDetailsForm
from app import app
web_dir = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), 'instagram_web')
users_blueprint = Blueprint('users',
							__name__,
							template_folder='templates/users')

csrf = CsrfProtect(app)

@users_blueprint.route('/new', methods=['GET'])
def new():
	return render_template('new.html')

@users_blueprint.route('/', methods=["GET"])
def index():
	return render_template('index.html')

@users_blueprint.route('/', methods=['POST'])
def create():
	pass

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
	pass

@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
	pass

# Need to be logged in
# check user log in ID == requested user ID
# if true: proceed, else: prompt

# capture logged in user ID, then direct to the page
# + redirect to correct user if tries to violate
@login_required
# @users_blueprint.route('/<id>', methods=['POST']) # can we use username instead?
@users_blueprint.route('/update', methods=['POST', 'GET'])
def update():
	form = UpdateDetailsForm()
	if request.method == 'POST' and form.validate():
		password = check_password_hash(current_user.password, form.data['password'])
		if not password:
			flash("Please ensure that password is correctly typed for updates to take effect", "alert")
			return redirect(url_for('users.login'))
		else:
			'''update the user'''
			updated_user = User.update().where(username=form.data['username'],
				email=form.data['email'],
				password=generate_password_hash(form.data['password']))
			# updated_user = User(
			# 	username=form.data['username'],
			# 	email=form.data['email'],
			# 	password=generate_password_hash(form.data['password'])
			# )
			updated_user.save()
			flash("Update successful", "success")
			return redirect(url_for('users.index'))
	if request.method == 'GET':
		username = current_user.username
		email = current_user.email
		# then need to display 'username' and 'email' on the form
		return render_template('update.html', form=form, username=username, email=email)

@users_blueprint.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST' and form.validate():
		new_user = User(
			username=form.data['username'],
			email=form.data['email'],
			password=generate_password_hash(form.data['password'])
		)
		new_user.save()
		flash("Thanks for registering", "success")
		return redirect(url_for('users.login'))
	return render_template('register.html', form=form)

@users_blueprint.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method == 'POST':
		if form.validate():
			user = User.get_or_none(User.email == form.data['email'])
			if user and check_password_hash(user.password, form.data['password']):
				login_user(user)
				flash("You've been logged in!", "success")
				return redirect(request.args.get('next') or url_for('users.index'))
			else:
				flash("Your email or password doesn't match!", "warning")
	return render_template('login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out!", "success")
	return redirect(url_for('users.login'))
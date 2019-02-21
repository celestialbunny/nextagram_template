from flask import Blueprint, render_template
from flask_bcrypt import check_password_hash
from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_login import (LoginManager, login_user, current_user, logout_user, login_required)
from flask_wtf.csrf import CsrfProtect
import os

from models.user import User
from instagram_web.blueprints.users.forms import RegistrationForm, LoginForm

web_dir = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), 'instagram_web')
users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CsrfProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


@users_blueprint.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST'and form.validate():
		new_user = User(
			username=request.form['username'],
			email=request.form['email'],
			password=request.form['password']
		)
		new_user.save()
		flash("Thanks for registering", "success")
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@users_blueprint.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# if form.validate_on_submit():
	if request.method == 'POST':
		if form.validate():
			try:
				user = User.get(User.email == form.email.data)
			except models.DoesNotExist:
				flash("Your email or password doesn't match!", "error")
			else:
				if check_password_hash(user.password, form.password.data):
					login_user(user)
					flash("You've been logged in!", "success")
					return redirect(url_for('index'))
				else:
					flash("Your email or password doesn't match!", "error")
	return render_template('login.html', form=form)

@users_blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out!", "success")
	return redirect(url_for('index'))
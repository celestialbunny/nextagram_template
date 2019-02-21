import os
import config
from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, current_user, logout_user, login_required)

from models.base_model import db
from models.user import User
from models.forms import RegistrationForm, LoginForm

web_dir = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
	app.config.from_object("config.ProductionConfig")
else:
	app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
	db.connect()


@app.after_request
def after_request(response):
	db.close()
	return response


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	# if form.validate_on_submit():
	if form.validate():
		flash("Thanks for registering", "success")
		User.create_user(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data
		)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route("/login")
def login():
	pass
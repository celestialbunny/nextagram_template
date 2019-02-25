import os
import config
from flask import (Flask, render_template, flash, redirect, url_for, request, session, escape, Blueprint, abort)
from flask_login import (login_user, logout_user, login_required, current_user, LoginManager)
from flask_wtf import CSRFProtect


from models.base_model import db

web_dir = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
csrf = CSRFProtect(app)

if os.getenv('FLASK_ENV') == 'production':
	app.config.from_object("config.ProductionConfig")
else:
	app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
	# db.close()
	db.connect()

@app.after_request
def after_request(response):
	db.close()
	return response

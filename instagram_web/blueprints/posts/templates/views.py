from flask import Blueprint, render_template, session, escape
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf.csrf import CsrfProtect
import os
from peewee import IntegrityError

from models.user import User
from instagram_web.blueprints.posts.forms import CreatePostForm
from app import app
web_dir = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), 'instagram_web')
posts_blueprint = Blueprint('posts',
							__name__,
							template_folder='templates/posts')

csrf = CsrfProtect(app)

@posts_blueprint.route('/new', methods=['GET'])
def new():
	return render_template('new.html')

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
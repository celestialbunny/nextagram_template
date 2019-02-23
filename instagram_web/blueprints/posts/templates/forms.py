from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class CreatePostForm(FlaskForm):
	image = FileField(
		'Image',
		validators=[
			DataRequired()
		]
	)
	description = TextAreaField(
		'description'
	)
	submit = SubmitField('Create Post')

class UpdatePostForm(FlaskForm):
	image = FileField(
		'Image',
		validators=[
			DataRequired()
		]
	)
	description = TextAreaField(
		'description'
	)
	submit = SubmitField('Update Post')
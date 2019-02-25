from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class PostForm(FlaskForm):
	# image = FileField(
	# 	'Image',
	# 	validators=[
	# 		DataRequired()
	# 	]
	# )
	title = StringField(
		'Title',
		validators=[
			DataRequired()
		]
	)
	description = TextAreaField(
		'description'
	)
	submit = SubmitField('Post')
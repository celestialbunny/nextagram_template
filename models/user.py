from models.base_model import BaseModel
import peewee as pw
import datetime
from flask_login import UserMixin

class User(UserMixin, BaseModel):
	username = pw.CharField(unique=True, null=False)
	email = pw.CharField(unique=True, null=False)
	password = pw.CharField(unique=True, null=False)

	# def validate(self):
	# 	user = User.get_or_none(User.username == self.data)
	# 	email = User.get_or_none(User.email == self.data)
	# 	if user:
	# 		raise pw.IntegrityError('Username is already taken. Please choose another username')
	# 	if email:
	# 		raise pw.IntegrityError('Email is already taken. Please choose another username')

		# try:
		# 	pass
		# except expression as identifier:
		# 	pass
		# else:
		# 	pass
		# finally:
		# 	pass
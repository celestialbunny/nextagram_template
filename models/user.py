from models.base_model import BaseModel
from flask_bcrypt import generate_password_hash
import peewee as pw


class User(BaseModel):
	username = pw.CharField(unique=True, null=False)
	email = pw.CharField(unique=True, null=False)
	password = pw.CharField(unique=True, null=False)

	@classmethod
	def create_user(cls, username, email, password, admin=False):
		try:
			cls.create(
				username=username,
				email=email,
				password=generate_password_hash(password),
				is_admin=admin
			)
		# Integrity error will be thrown if the username and email are NOT actually unique (duplicated in other words)
		except IntegrityError:
			raise ValueError("Either username and/or email has been taken")
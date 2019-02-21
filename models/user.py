from models.base_model import BaseModel
import peewee as pw
import datetime
from flask_login import UserMixin


class User(UserMixin, BaseModel):
	username = pw.CharField(unique=True, null=False)
	email = pw.CharField(unique=True, null=False)
	password = pw.CharField(unique=True, null=False)
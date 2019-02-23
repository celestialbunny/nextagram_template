from models.base_model import BaseModel
from peewee import CharField, IntegerField, TextField, ForeignKeyField
from models.user import User

class Post(BaseModel):
	owner_id = ForeignKeyField(User, backref='posts', unique=True)
	description = TextField(unique=False, null=True)
	status = IntegerField(unique=False, null=True)
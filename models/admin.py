from tortoise import fields, models
from passlib.hash import bcrypt

class Admin(models.Model):
    admin_id = fields.CharField(max_length=64,pk=True)
    username = fields.CharField(max_length=64, unique=True)
    name = fields.CharField(max_length=128)
    email = fields.CharField(max_length=128)
    password = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True,null=True)

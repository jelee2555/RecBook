from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30)
    user_birth = models.DateField()
    user_gender = models.CharField(max_length=5)
    user_password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'usertbl'


# class UserGet(models.Model):
#     user_id = models.IntegerField(primary_key=True, unique=True)
#     user_name = models.CharField(max_length=30, unique=True)
#     user_birth = models.DateField(unique=True)
#     user_gender = models.CharField(max_length=5)
#     user_password = models.CharField(max_length=20, unique=True)
#
#     class Meta:
#         managed = False
#         db_table = 'usertbl'

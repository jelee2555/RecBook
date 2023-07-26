from django.db import models

from accounts.models import User


# Create your models here.
class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_title = models.CharField(max_length=500)
    book_writer = models.CharField(max_length=50)
    book_publish = models.CharField(max_length=100)
    book_class = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'booktbl'

class Recommand(models.Model):
    recommand_id = models.IntegerField(primary_key=True)
    recommand_gender = models.CharField(max_length=5)
    recommand_age = models.CharField(max_length=20)
    recommand_class = models.IntegerField()
    recommand_class_cnt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'recommandtbl'

class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    book = models.ForeignKey(Book, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'liketbl'
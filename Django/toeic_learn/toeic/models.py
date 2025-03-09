# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class User(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(8), MaxLengthValidator(16)]
        )
    username = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.email


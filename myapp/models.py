from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Account'

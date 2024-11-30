from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=12, unique=True)
    invite_code = models.IntegerField(unique=True, null=True, blank=True)
    activated_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.phone_number

    @staticmethod
    def generate_invite_code():
        return randint(100000, 999999)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone_number
        super().save(*args, **kwargs)


class AuthCode(models.Model):
    code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = randint(1000, 9999)
        super().save(*args, **kwargs)

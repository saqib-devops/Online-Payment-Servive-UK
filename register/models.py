from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    CURRENCY_TYPE = (
        (1, 'USD'),
        (2, 'GBP'),
        (3, 'EURO'),
    )
    email = models.EmailField(unique=True, max_length=200)
    total_amount = models.FloatField(default=1000)
    sent_amount = models.FloatField(default=0)
    received_amount = models.FloatField(default=0)
    remaining_amount = models.FloatField(default=1000)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE,default=1)

    REQUIRED_FIELDS = ['username',]
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

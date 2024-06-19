from django.contrib.auth.models import User
from django.db import models

from core.models import AbstractBaseModel


# Create your models here.
class Customer(AbstractBaseModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email

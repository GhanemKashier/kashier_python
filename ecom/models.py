from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
# Create your models here.





class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.JSONField()
    def __str__(self):
        return self.name


class Merchant(models.Model):
    KEY=models.CharField(max_length=40)
    VALUE=models.CharField(max_length=40)

    def __str__(self):
        return self.name

from django.db import models

class Beverage(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()

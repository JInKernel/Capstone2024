from django.db import models
from django.contrib.auth.models import User

class Beverage(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    beverage = models.ForeignKey(Beverage, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    face_embedding_vector = models.BinaryField()
    birthdate = models.DateField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

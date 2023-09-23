from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Flower(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    photo = models.ImageField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)


class PaidOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    date=models.DateField()


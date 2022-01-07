from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from crispy_forms.helper import FormHelper

# Create your models here.

class Search(models.Model):
    search_address = models.CharField(max_length=200, null=True)
    search_country = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.search_address


class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_pwd = models.CharField(max_length=10)

    def __str__(self):
        return self.user_name


class Registration(models.Model):
    reg_name = models.CharField(max_length=200, null=False)
    reg_pwd = models.CharField(max_length=200, null=False)
    reg_pwd2 = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.reg_name

RATE_CHOICES = [
    (1, '1 - Very Bad'),
    (2, '2 - Bad'),
    (3, '3 - OK'),
    (4, '4 - Good'),
    (5, '5 - Very Good')
]


class RateCity(models.Model):
    user = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    overall = models.FloatField(null=True)
    nightlife = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    food = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    culture = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    people = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    accommodation = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return str(self.city)

class DistinctRateCity(models.Model):
    distinct_city = models.CharField(max_length=200, null=False)
    distinct_country = models.CharField(max_length=200, null=False)
    distinct_counter = models.IntegerField()
    distinct_overall = models.FloatField(null=True)
    distinct_nightlife = models.FloatField()
    distinct_food = models.FloatField()
    distinct_culture = models.FloatField()
    distinct_people = models.FloatField()
    distinct_accommodation = models.FloatField()

    def __str__(self):
        return str(self.distinct_city)

    


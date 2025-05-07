from django.db import models

# Create your models here.


class CountryModel(models.Model):
    name = models.CharField(max_length=255)
    cca2 = models.CharField(max_length=255)
    capital = models.CharField(max_length=255, null=True, blank=True)
    population = models.BigIntegerField()
    timezone = models.CharField(max_length=100)
    flag = models.CharField(max_length=10)
    region = models.CharField(max_length=100, null=True, blank=True)
    languages = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.


class CountryModel(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    cca2 = models.CharField(max_length=255, null=True, blank=True)
    capital = models.CharField(max_length=255, null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    flag = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name

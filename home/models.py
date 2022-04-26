from django.db import models

class Prices(models.Model):
    name = models.CharField(max_length=254)
    price = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

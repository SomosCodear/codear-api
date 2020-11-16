from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateTimeField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Argentina')
    link = models.URLField()
    external_reference = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

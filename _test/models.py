from django.db import models
from datetime import date

__all__ = ("Car",)


class Car(models.Model):
    plate = models.CharField(max_length=250)
    year = models.PositiveIntegerField(default=date.today().year, blank=True)

    class Meta:
        app_label = "_test"

    def __str__(self):
        return self.plate

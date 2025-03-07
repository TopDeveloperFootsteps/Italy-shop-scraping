from django.db import models

class UnitItem(models.Model):
    unit = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
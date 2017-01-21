from __future__ import unicode_literals

from django.db import models
from django.utils import timezone



class Gate(models.Model):
    name = models.CharField(max_length=20)
    matrix = models.TextField()

    def __str__(self):
        return self.name
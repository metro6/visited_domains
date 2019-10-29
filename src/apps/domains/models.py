from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=127)
    visited = models.IntegerField(default=0)
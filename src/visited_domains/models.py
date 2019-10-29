from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=127)
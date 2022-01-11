from django.db import models
from django.conf import settings

# Create your models here.
class Directory(models.Model):
    name = models.CharField(max_length=255,)
    parent = models.IntegerField(blank=True,)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    class Meta:
        ordering = ['owner', 'parent', 'name']



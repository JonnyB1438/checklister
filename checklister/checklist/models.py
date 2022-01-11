from django.db import models
from django.conf import settings

# Create your models here.
class Directory(models.Model):
    """
    This model stores a structure of directory, where:
        - parent is a parent directory id
        - owner is an user id from AUTH_USER_MODEL
    """
    name = models.CharField(max_length=255,)
    parent = models.IntegerField(blank=True,)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    class Meta:
        ordering = ['owner', 'parent', 'name']

class CheckListTemplate(models.Model):
    """
    This model stores checklist templates with reference to a directory, where:
        - list is a checklist JSON dump
        - directory is a directory id from Directory model
    """
    name = models.CharField(max_length=255,)
    list = models.TextField(blank=True,)
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE,)

    class Meta:
        ordering = ['directory', 'name',]

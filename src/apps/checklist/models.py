from django.db import models
from django.conf import settings


# Create your models here.
class Directory(models.Model):
    """
    This model stores a structure of directory, where:
        - parent is a parent directory id
        - owner is a user id from AUTH_USER_MODEL
    """
    name = models.CharField(max_length=255, verbose_name='Directory name')
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, verbose_name='Parent directory')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')

    class Meta:
        default_related_name = 'directories'
        ordering = ['owner', 'name']
        verbose_name = 'Directory'
        verbose_name_plural = 'Directories'


class CheckListTemplate(models.Model):
    """
    This model stores checklist templates with reference to a directory, where:
        - list is a checklist JSON dump
        - directory is a directory id from Directory model
    """
    name = models.CharField(max_length=255, verbose_name='Name')
    data = models.TextField(default='', verbose_name='Checklist')
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE, verbose_name='Parent directory')

    class Meta:
        default_related_name = 'checklists'
        ordering = ['directory', 'name', ]
        verbose_name = 'CheckList Template'
        verbose_name_plural = 'CheckList Templates'

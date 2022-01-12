from django.contrib import admin
from .models import Directory, CheckListTemplate


class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'owner',)
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'parent', 'owner',)
    list_editable = ('owner',)
    list_filter = ('parent', 'owner',)


class CheckListTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'directory',)
    list_display_links = ('id', 'directory',)
    search_fields = ('name',)
    list_editable = ('name', )
    list_filter = ('directory',)


# Register your models here.
admin.site.register(Directory,DirectoryAdmin)
admin.site.register(CheckListTemplate, CheckListTemplateAdmin)

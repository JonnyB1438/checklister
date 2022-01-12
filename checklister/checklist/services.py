from .models import Directory


def get_user_root_directory(user):
    directories = Directory.objects.filter(owner=user, parent=None).values('id', 'name')
    return directories

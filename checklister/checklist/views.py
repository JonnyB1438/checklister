from django.shortcuts import render
from .services import *


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_root_directory = get_user_root_directory(request.user)
        return render(request, 'checklist/checklist.html', {'list_directories': user_root_directory})
    else:
        return render(request, 'checklist/checklist.html')

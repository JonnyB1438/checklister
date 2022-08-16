
from django.urls import path, include
from .views import AjaxHandlerView
from config import settings

urlpatterns = [
    path('', AjaxHandlerView.as_view(), name='checklist'),
]



from django.urls import path
from .views import AjaxHandlerView


urlpatterns = [
    path('', AjaxHandlerView.as_view(), name='checklist'),
]


from django.urls import path
from . import views
from .views import AjaxHandlerView


urlpatterns = [
    # path('', views.index, name='checklist'),
    path('', AjaxHandlerView.as_view(), name='checklist'),
]

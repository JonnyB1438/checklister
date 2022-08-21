
from django.urls import path, include

from .drfviews import *
from .views import AjaxHandlerView
from config import settings


urlpatterns = [
    path('', AjaxHandlerView.as_view(), name='checklist'),
    path('api/v1/checklists/<int:dir_id>/', ChecklistListAPIView.as_view()),
    path('api/v1/checklist/<int:pk>/', ChecklistRUDAPIView.as_view()),

    path('api/v1/dirs/<int:parent_id>/', DirectoryListAPIView.as_view()),
    path('api/v1/dir/<int:pk>/', DirectoryRUDAPIView.as_view()),

    path('api/v1/structure/', DirectoryAPIView.as_view()),
]


from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SingUpView.as_view(), name="signup"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('profile/done/', views.ProfileDoneView.as_view(), name="profile_done"),
]

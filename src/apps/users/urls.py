from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('signup/', views.SingUpView.as_view(), name="signup"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('profile/done/', views.ProfileDoneView.as_view(), name="profile_done"),
]

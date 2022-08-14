from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import ModifiedUserCreationForm, ModifiedUserChangeForm
from django.contrib.auth import get_user_model


class SingUpView(CreateView):
    form_class = ModifiedUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ModifiedUserChangeForm
    success_url = reverse_lazy("profile_done")
    template_name = "users/profile.html"
    model = get_user_model()

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDoneView(SuccessURLAllowedHostsMixin, TemplateView):
    template_name = 'users/profile_done.html'
    pass

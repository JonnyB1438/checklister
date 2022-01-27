from django.contrib.auth.views import SuccessURLAllowedHostsMixin, PasswordContextMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from .forms import ModifiedUserCreationForm


class SingUp(CreateView):
    form_class = ModifiedUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

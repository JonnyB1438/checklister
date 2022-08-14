from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from django import forms

User = get_user_model()


class ModifiedUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email",)


class ModifiedUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email",)




# class UpdateUserForm(UpdateViewForm):
#     class Meta(UpdateView.Meta):
#         model = User
#         fields = ["first_name", "last_name", "email",]
        # fields = ["first_name", "last_name", "username", "email",]

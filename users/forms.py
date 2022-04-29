from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserSignInForm(UserCreationForm):
    username = forms.CharField(label="username", min_length=4, max_length=75, required=True)
    email = forms.EmailField(label="email", required=True)
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)
    f_name = forms.CharField(max_length=75)
    l_name = forms.CharField(max_length=75)

    def username_clean(self):
        username = self.cleaned_data["username"].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("An user with this username already exist")
        return username

    def email_clean(self):
        email = self.cleaned_data["email"].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("This email is used already used by someone")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        return user

    class Meta:
        model = User
        fields = [
            "f_name",
            "l_name",
            "username",
            "email",
            "password1",
            "password2",
        ]
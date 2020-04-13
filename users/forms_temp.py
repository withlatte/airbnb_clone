from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(UserCreationForm):
    # username = forms.EmailField(label="Email")
    username = forms.CharField(widget=forms.EmailInput)

    # class Meta:
    #     model = models.User
    #     fields = ("username",)
    #     # field_classes = {"username": UsernameField}
    #
    # def save(self, *args, **kwargs):
    #     user = super().save(commit=False)
    #     email = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password2")
    #     user.username = email
    #     user.set_password(password)
    #     user.save()

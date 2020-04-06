from django import forms
from . import models


class LoginForm(forms.Form):
    """ Login Form Definition """

    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return (
                    self.cleaned_data
                )  # if you use clean(self) method, you must return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Wrong password"))
        except models.User.DoesNotExist:
            self.add_error(
                "username", forms.ValidationError(f"{username} does not exist.")
            )

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email Address"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

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
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "username",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "username": forms.EmailInput(attrs={"placeholder": "Email Address"}),
        }


class UpdatePasswordForm(PasswordChangeForm):
    """ Update Password Form Definition """

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Current Password"})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm New Password"})
    )


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False, widget=forms.FileInput, label="Upload Profile Image"
    )

    class Meta:
        model = models.User
        fields = [
            "first_name",
            "last_name",
            "avatar",
            "gender",
            "bio",
            "birthdate",
            "language",
            "currency",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "bio": forms.Textarea(attrs={"placeholder": "Biography"}),
            "birthdate": forms.DateInput(attrs={"placeholder": "yyyy-mm-dd"}),
        }

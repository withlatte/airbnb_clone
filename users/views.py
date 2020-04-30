import os
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm

    # success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome back {user.first_name}!")
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"Good Bye {request.user.first_name}!")
    logout(request)
    return redirect(reverse("users:login"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("username")  # todo email >> username
        password = form.cleaned_data.get("password2")  # todo password >> password2
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        if user.email == "":  # todo add email field same as username
            user.email = email
        user.verify_email()
        return super().form_valid(form)


def complete_verification(self, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    #     todo : add success message
    except models.User.DoesNotExist:
        # todo : add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"

    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get authorization code.")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please login with your {user.login_method} account."
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            email=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    messages.success(request, f"Welcome back {user.first_name}!")
                    login(request, user)

                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile.")
        else:
            raise GithubException("Can't get authorization code.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"

    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        client_id = os.environ.get("KAKAO_ID")
        client_secret = os.environ.get("KAKAO_SECRET")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri={redirect_uri}",
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise KakaoException("Can't get authorization token.")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://kapi.kakao.com/v2/user/me",
                    headers={"Authorization": f"Bearer {access_token}",},
                )
                profile_json = profile_request.json()
                kakao_account = profile_json.get("kakao_account")
                properties = profile_json.get("properties")
                profile = kakao_account.get("profile")
                email = kakao_account.get("email", None)
                if email is not None:
                    name = profile.get("nickname")
                    gender = kakao_account.get("gender")
                    profile_image = properties.get("profile_image")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_KAKAO:
                            raise KakaoException(
                                f"Please login with your {user.login_method} account."
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=email,
                            first_name=name,
                            email=email,
                            gender=gender,
                            login_method=models.User.LOGIN_KAKAO,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        if profile_image is not None:
                            photo_request = requests.get(profile_image)
                            user.avatar.save(
                                f"{email}-avatar", ContentFile(photo_request.content)
                            )
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}!")
                    return redirect(reverse("core:home"))
                else:
                    raise KakaoException("Please provide your email.")
        else:
            raise KakaoException("Can't get authorization code.")
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    """ User Profile View Definition """

    model = models.User
    context_object_name = "user_obj"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hello"] = "Hello! Aloha! Pagi!"
        return context


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    """ Update Profile View Definition """

    model = models.User
    form_class = forms.UpdateProfileForm
    template_name = "users/update-profile.html"
    success_message = "Profile updated."

    def get_object(self, queryset=None):
        return self.request.user


class UpdatePasswordView(
    mixins.LoggedInOnlyView,
    mixins.EmailLoginOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    """ Change Password View Definition """

    template_name = "users/update-password.html"
    form_class = forms.UpdatePasswordForm
    success_message = "Password Updated"

    def get_success_url(self):
        # return reverse(self.request.user.get_absolute_url())   --> 니꼴라스 코드 오류발생함
        return reverse("users:profile", kwargs={"pk": self.request.user.pk})


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))

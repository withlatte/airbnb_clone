from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy


class EmailLoginOnlyView(UserPassesTestMixin):
    """
    Email Login Only View Definition :
    카카오나 깃허브 로그인 사용자가 url 주소를 바꿔 password 변경 페이지로 이동하는 것을 막는다.
    """

    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        lm = self.request.user.login_method
        messages.error(
            self.request, f"{lm} 로그인 사용자는 {lm} 계정에서 암호를 변경해 주시기 바랍니다.",
        )
        return redirect(reverse("core:home"))


class LoggedOutOnlyView(UserPassesTestMixin):
    """
    LoggedOutOnlyView Class Definition:
    Logged out user only can go this page
    """

    def test_func(self):
        # 인증된 유저가 아니면 "True" 를 리턴한다. 인증된 유저면 "False"
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):
    """
    Logged In Only View Definition :
    클라스 뷰에서 reverse_lazy 를 주로사용하고, function based view 에서는 reverse 를 주로 사용
    클라스 뷰에서도 success_url 과 같이 인자에 assign 할 때에는 reverse_lazy 를 사용하고,
    get_success_url() 처럼 function 안에서 사용할 때는 reverse 를 사용한다.
    """

    login_url = reverse_lazy("users:login")

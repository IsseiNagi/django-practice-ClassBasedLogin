from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'


class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm


# # LoginViewを使ってログインさせる方法に切り替えるため、以下のView継承方式はコメントアウトする
# # FormViewを継承してログインビューを作る
# class UserLoginView(FormView):
#     template_name = 'user_login.html'
#     form_class = UserLoginForm

#     def post(self, request, *args, **kwargs):
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(email=email, password=password)
#         next_url = request.POST['next']  # 注釈A
#         if user is not None and user.is_active:
#             login(request, user)
#         if next_url:  # 注釈A
#             return redirect(next_url)  # 注釈A
#         return redirect('accounts:home')

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm


# # LogoutViewを使ってログアウトさせる方法に切り替えるため、以下のView継承方式はコメントアウトする
# # Viewを継承してログアウトビューを作る
# class UserLogoutView(View):

#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('accounts:user_login')

class UserLogoutView(LogoutView):
    pass  # 今回は、LogoutViewを継承するだけで、特に中身は書かなくていい


# ユーザーページを作る。ユーザーページはログインを必須とする。その制限の掛け方は３通りある。

# ②クラスにデコレーターをつけて、メソッドを指定するやり方
# @method_decorator(login_required, name='dispatch')
class UserView( LoginRequiredMixin, TemplateView):  # ③LoginRequiredMixinを継承させるやり方
    template_name = 'user.html'

    # ①メソッドにデコレーターをつけるやり方　UserViewのdispatchメソッドがよばれるときに、loginを必須とする
    # dispatchはPOSTだったらPOSTの処理を、GETだったらGETの処理を行うメソッド。これをオーバーライドして、制限をかけている
    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# ログインしていない状態でユーザー画面を叩くと、loginというurlにリダイレクトするデフォルトになっているので、404エラーになる
# settings.pyで、LOGIN_URL = '/accounts/user_login'として、カスタマイズしたログインurlを指定する

# 注釈A
# ログインせずにユーザー画面を叩くと、ログイン画面に遷移するが、ログインした後、homeに遷移するので、ユーザー画面に遷移させるようにする
# http://127.0.0.1:8000/accounts/user_login/?next=/accounts/user/  ?next以降は、本来遷移したかったurlの情報が来ている

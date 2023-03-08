from django.urls import path

from SRTMacro.views import print_page, srt_list_join, srt_macro
from SRTMacro.views import login_page
from SRTMacro.views import login_auth
from django.urls import path
from django.contrib.auth import views as auth_views
app_name="SRTMacro"
# 들어오고자 하는 경로: "127.0.0.1:8000/account/hello_world" <=> accountapp:firstpage_name

urlpatterns = [
    path('', print_page, name='index'),
    path('login/', login_page, name='login'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('loginauth/', login_auth, name='loginauth'),
    path('srtList/', srt_list_join, name='srtJoin'),
    path('srtMc/', srt_macro, name='srtMacroOn'),
]
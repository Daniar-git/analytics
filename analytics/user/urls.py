from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('info/', views.UserInfoView.as_view(), name='user_info'),
    path('token/info/', views.UserTokenInfo.as_view(), name='user_info'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
]
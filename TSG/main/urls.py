import profile
from django.contrib import admin
from django.urls import path, include,re_path
from . import views
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    # path('auth/', include('rest_framework.urls')),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('accounts/profile/', views.profile, name='profile'),#личный кабинет
    path('accounts/profile/quiz/<str:pk>/', views.vote, name='vote'),
    path('accounts/profile/quiz/', views.quiz, name='quiz'),
    path('about', views.about, name='about'),
    path('accounts/profile/feedback', views.feedback, name='feed'),

    # path('accounts/profile/quiz/', GetQuestion.as_view()),
    # path('accounts/profile/answer/', QuestionAnswer.as_view()),

]


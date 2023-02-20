from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from requests import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import datetime

from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

from .forms import *
from .models import *
from .utils import *
from .serializers import *


# Create your views here.
def home(request):
    news = News.objects.all()[::-1]
    # news = News.objects.order_by("-id")
    return render(request, 'main/home.html', {'news': news})


def feedback(request):
    if request.user.is_authenticated != True:
        return redirect("login")
    if request.method == 'POST':
        feed = Feedback()
        if request.POST['title'] == '' or request.POST['question'].strip() == '':
            return redirect('feed')
        feed.title = request.POST['title']
        feed.question = request.POST['question'].strip()
        feed.time_quest = datetime.datetime.now()
        feed.save()
        return redirect('feed')
    feedback = Feedback.objects.all()[::-1]
    return render(request, 'profile/feedback.html', {'feedback': feedback})


def profile(request):
    if request.user.is_authenticated != True:
        return redirect("login")
    if request.method == 'POST':
        telenum = request.POST['telenum']
        email = request.POST['email']
        if not (len(telenum) <= 10 and len(telenum) > 0 and telenum.isdigit() == True and "@" in email and "."
                in email and len(email) > 8 and telenum != '8' + str(request.user.telenum) and email !=  request.user.email):
            return redirect('profile')
        if len(telenum) <= 10 and len(telenum) > 0 and telenum.isdigit() == True:
            request.user.telenum = '8' + telenum
        if "@" in email and "." in email and len(email) > 8:
             request.user.email = email

        request.user.save()
        return redirect('profile')
    user_info = request.user
    num = str(user_info.telenum)[1::]
    return render(request, 'profile/profile.html', {'user_info': user_info, "num" : num})


class LoginUser(LoginView):
    from_class = LoginUserForm
    template_name = 'profile/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')


def LogoutUser(request):
    logout(request)
    return redirect('home')


def quiz(request):
    if request.user.is_authenticated != True:
        return redirect("login")
    questions = Question.objects.all()[::-1]
    answers = []
    for question in questions:
        if Answer.objects.filter(question=question, user=request.user):
            answers.append(question)
    return render(request, 'profile/quiz.html', {'questions': questions, 'answers': answers})


def vote(request, pk):
    if request.user.is_authenticated != True:
        return redirect("login")
    question = Question.objects.get(id=pk)
    options = Choice.objects.filter(question=question)

    if Answer.objects.filter(question=question, user=request.user):
        choice = Answer.objects.get(question=question, user=request.user)
        return render(request, 'profile/vote_applied.html', {'question': question, 'options': options, 'choice': choice.choice})
    else:
        if request.method == 'POST':
            if ('choice' in request.POST):
                inputvalue = request.POST['choice']
                answer = Answer(user=request.user, question=question, choice=options.get(id=inputvalue))
                answer.save()
                return redirect(request.META['HTTP_REFERER'])
        return render(request, 'profile/vote.html', {'question': question, 'options': options})


def about(request):
    return render(request, 'main/about.html')


def test(request):
    return render(request, 'test.html')
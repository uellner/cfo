from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, RecoverForm


def login_view(request):
    wrong_data = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                wrong_data = True
    else:
        form = LoginForm()
    return render(
        request,
        'login.html',
        {
            "form":form,
            "wrong_data": wrong_data
        }
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def recover_view(request):
    wrong_data = None
    if request.method == "POST":
        form = RecoverForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            if user and user.is_active:
                new_password = User.objects.make_random_password()
                user.set_password(new_password)
                user.save()
                subject = "[Clube de Finanças Online] Recuperação de Senha"
                message = "Sua nova senha é: " + new_password
                send_mail(subject, message, settings.EMAIL_FROM, [user.email])
                return HttpResponseRedirect('/')
            else:
                wrong_data = True
    else:
        form = RecoverForm()
    return render(
        request,
        'recover.html',
        {
            "wrong_data": wrong_data
        }
    )

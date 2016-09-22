from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from annoying.decorators import render_to
from .forms import LoginForm, RecoverForm, StudentEditForm, UserEditForm
from .models import Student


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


@render_to('edit.html')
@login_required
def edit(request, student=None):
    """
        Form para edição de um estudante.
    """
    student_instance = student and get_object_or_404(Student, id=student) or None
    user_instance = student_instance and student_instance.user or None
    if request.method == "POST":
        forms = [
            UserEditForm(request.POST, instance=user_instance),
            StudentEditForm(request.POST, instance=student_instance)
        ]
        if all([form.is_valid() for form in forms]):
            user = forms[0].save(commit=False)
            password = forms[0].cleaned_data['password']
            if password:
                user.set_password(password)
            user.save()
            # Save the new student
            student = forms[1].save(commit=False)
            student.user = user
            student.save()
            return redirect('dashboard',)
    else:
        forms = [UserEditForm(instance=user_instance), StudentEditForm(instance=student_instance)]

    action = student and reverse('user_edit', kwargs={'student': student}) or reverse('user_new')
    return {
        'title': 'Perfil Estudante',
        'action': action,
        'forms': forms,
    }

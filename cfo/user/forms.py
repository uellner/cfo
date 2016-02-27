from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


class RecoverForm(forms.Form):
    username = forms.CharField(label='Usuario')

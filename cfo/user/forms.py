from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout, Fieldset, ButtonHolder, Submit, Button, Field, Div, HTML
)
from .models import Student
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


class RecoverForm(forms.Form):
    username = forms.CharField(label='Usuario')


class UserNewForm(forms.ModelForm):
    prefix = 'user'

    def __init__(self, *args, **kwargs):
        super(UserNewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('id', type="hidden"),
            Fieldset(
                '',
                Div('first_name', css_class="col-sm-6"),
                Div('last_name', css_class="col-sm-6"),
                Div('email', css_class="col-sm-12"),
                Div('username', css_class="col-sm-12"),
                Div('password', css_class="col-sm-6"),
                Div('password_confirmation', css_class="col-sm-6"),
                css_class="col-sm-12"
            ),
        )

    def clean_password_confirmation(self):
        """
            Verify if both password fields were filled and are the same.
        """
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirmation')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Confirmação de senha inválida.")
        return password2

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password_confirmation',
            'first_name', 'last_name', 'id'
        )

    # Person fields
    first_name = forms.CharField(required=True, max_length=30, label="Nome")
    last_name = forms.CharField(required=False, max_length=30, label="Sobrenome")
    # Login fields
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha")


class UserEditForm(UserNewForm):

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('id', type="hidden"),
            Fieldset(
                'Informações de acesso',
                Div('username', css_class="col-sm-12"),
                Div('password', css_class="col-sm-12"),
                Div('password_confirmation', css_class="col-sm-12"),
                css_class="col-sm-3"
            ),
            Fieldset(
                'Informações pessoais',
                Div('first_name', css_class="col-sm-12"),
                Div('last_name', css_class="col-sm-12"),
                Div('email', css_class="col-sm-12"),
                css_class="col-sm-4"
            ),

        )

    password = forms.CharField(widget=forms.PasswordInput, label="Senha", required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirmar Senha", required=False)
    username = forms.CharField(widget=forms.TextInput, max_length=30, help_text='')


class StudentNewForm(forms.ModelForm):
    prefix = 'student'

    def __init__(self, *args, **kwargs):
        super(StudentNewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('id', type="hidden"),
            Fieldset(
                '',
                Div('phone', css_class="col-sm-12"),
                css_class="col-sm-12"),
            ButtonHolder(
                Div(
                    Submit('submit', 'Salvar', css_class='save btn btn-info'),
                    css_class="col-sm-12"
                ),
                css_class="col-sm-12"

            ),
        )

    class Meta:
        model = Student
        exclude = ('user',)


class StudentEditForm(StudentNewForm):

    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Field('id', type="hidden"),
            Fieldset(
                'Informações do Aluno',
                Div('phone', css_class="col-sm-6"),
                css_class="col-sm-5"),
            ButtonHolder(
                Div(
                    Submit('submit', 'Salvar', css_class='save btn btn-info'),
                    css_class="col-sm-5"
                ),
                css_class="col-sm-12"
            ),
        )

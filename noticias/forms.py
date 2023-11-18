from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class PesquisaForm(forms.Form):
    palavras_chave = forms.CharField(max_length=100, label='Palavras-chave')

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label='Nome Completo', widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}),
        help_text="The password must contain at least 6 characters."
    )
    password2 = None

    class Meta:
        model = User
        fields = ("email", "full_name", "username", "password1")

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        
        if len(password) < 6:
            raise forms.ValidationError("The password must contain at least 6 characters.")
        self.fields['password1'].widget.attrs.update({'class': 'password-length'})
        return password
    
class ComentarioForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your comment here', 'rows': 4}))

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
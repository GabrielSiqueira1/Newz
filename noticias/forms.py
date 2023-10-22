from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms
from .models import Comentario

class PesquisaForm(forms.Form):
    palavras_chave = forms.CharField(max_length=100, label='Palavras-chave')

class ComentarioForm(forms.ModelForm):
     texto = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escreva seu comentário aqui'}))

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, label='Nome Completo')
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="A senha deve conter no mínimo 6 caracteres."
    )
    password2 = None 

    class Meta:
        model = User
        fields = ("email", "full_name", "username", "password1")

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:
            raise forms.ValidationError("A senha deve conter pelo menos 6 caracteres.")
        return password
    
class ComentarioForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

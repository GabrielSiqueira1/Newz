from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class ComentarioForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

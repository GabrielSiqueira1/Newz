from django import forms

class ComentarioForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea)

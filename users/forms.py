from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Document

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file', 'num_copies', 'color_type', 'double_sided']  # ❌ REMOVE 'paper_size'

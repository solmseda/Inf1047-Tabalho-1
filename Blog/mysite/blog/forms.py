from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','password1','password2'] 
   
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'corpo']
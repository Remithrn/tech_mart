from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms

class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2","is_superuser","is_active"]

class EditForm(UserChangeForm):
    password=None
    class Meta:
        model =User
        fields =["username","email","is_superuser","is_active"]
        widgets ={
            "username":forms.TextInput(attrs={'class':'form-control'}),
            "email":forms.EmailInput(attrs={'class':'form-control'})
        }
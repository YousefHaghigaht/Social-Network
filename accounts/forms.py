from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('The entered username already exist')
        return username
    
    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match')
        return p2
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('The entered email already exist')
        return email
    
class UserLoginForm(forms.Form):
    username = forms.CharField(label='username or email',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'your username or email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'your password'}))
    

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile 
        fields = ('bio' , 'age' )   
from django import forms
from django.contrib.auth.models import User
from .models import BlogPost

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    password_confirm = forms.CharField(widget = forms.PasswordInput, label = 'Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password =cleaned_data.get('password')
        confirm = cleaned_data.get('password_confirm')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords must match!')
        return cleaned_data
    
class PostForm(forms.ModelForm):
    pass
    class Meta:
        model = BlogPost
        fields = ['id', 'post_name', 'post_content', 'post_date']

    def clean(self):
        initially_cleaned = super().clean()
        pass # The main validation logic will be written here.
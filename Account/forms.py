

from typing import Any, Mapping
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList


    
    
User=get_user_model()

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control"})

    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=40,widget=forms.PasswordInput)




class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        max_length=150,
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password"
        )

    

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.data.get('password2')

        if password != password2:
            raise forms.ValidationError("Password mismatch")

        return password           

    def save(self, commit=True, *args, **kwargs):
        user = self.instance
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()

        return user

    




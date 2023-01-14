from pyexpat import model
from socket import fromshare
from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.ModelForm):
    model = get_user_model()
    username =  forms.CharField()
    class Meta():
        fields = ['password']
        model = get_user_model()

    def clean_username(self):
        username = self.cleaned_data['username']
        # exists
        if not self.model.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Account with the username does not exist")
        return username

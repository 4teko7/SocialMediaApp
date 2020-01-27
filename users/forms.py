from django import forms
from django.contrib.auth.models import User

class loginForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password",widget = forms.PasswordInput)

class registerForm(forms.Form):
    username = forms.CharField(max_length = 50,label = "username")
    password = forms.CharField(max_length = 20,label = "Password",widget = forms.PasswordInput)
    confirm = forms.CharField(max_length = 20,label = "Confirm",widget = forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        newUser = User.objects.filter(username = username)
        if(password and confirm and password != confirm):
            raise forms.ValidationError("Password don't Match !")
        elif(newUser.exists()):
            raise forms.ValidationError("This username : {} exists.".format(username))

        values = {
            "username" : username,
            "password" : password
        }
        return values
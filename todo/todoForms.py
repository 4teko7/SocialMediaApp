# from django import forms
# from django.contrib.auth.models import User

# class addTodoForm(forms.Form):
#     title = forms.CharField(max_length = 50,label = "Title")
#     content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}) , label = "content")


from django import forms
from .models import Todo

class addTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title","content"]
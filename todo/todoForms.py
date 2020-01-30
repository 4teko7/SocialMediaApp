from django import forms
from django.contrib.auth.models import User

class addTodoForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}) , label = "content")
    date  = forms.DateField(label = "date",widget=forms.SelectDateWidget)
# from django import forms
# from .models import Todo

# class addTodoForm(forms.ModelForm):
#     class Meta:
#         model = Todo
#         fields = ["content","date"]
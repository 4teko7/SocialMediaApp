from django import forms
from .models import Article

class addArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","content","isPrivate"]
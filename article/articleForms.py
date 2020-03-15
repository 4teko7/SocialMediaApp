from django import forms
from .models import Article

class addArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title","content","isPrivate","articleImage"]
        # widgets={"articleImage":forms.FileInput(attrs={'color':'yellow','height':'10rem'}),} 
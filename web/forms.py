from django import forms
from .models import Comment, Image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')


class SearchForm(forms.Form):
    query = forms.CharField()


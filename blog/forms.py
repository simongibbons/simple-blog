from django import forms

from .models import Comment


class PostForm(forms.Form):
    title = forms.CharField(label='title', max_length=200)
    text = forms.CharField(label='text', widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

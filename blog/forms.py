from django import forms


class PostForm(forms.Form):
    title = forms.CharField(label='title', max_length=200)
    text = forms.CharField(label='text', widget=forms.Textarea)


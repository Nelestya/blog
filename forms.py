from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentPostForm(forms.Form):
    pseudonyme = forms.CharField(max_length=25)
    email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea)

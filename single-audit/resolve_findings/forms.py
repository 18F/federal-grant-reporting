from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # There's no need for the user to edit any of the other fields.
        # The trailing comma is required for this to be recognized as a tuple.
        fields = ('body',)

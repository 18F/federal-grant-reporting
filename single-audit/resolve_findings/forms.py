from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # There's no need for the user to edit any of the other fields.
        # The trailing comma is required for this to be recognized as a tuple.
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'big_textarea width-full margin-top-1'}),
        }

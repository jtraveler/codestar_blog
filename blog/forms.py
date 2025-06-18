from django import forms
from .models import Comment, CollaborationRequest


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class CollaborationForm(forms.ModelForm):
    class Meta:
        model = CollaborationRequest
        fields = ('name', 'email', 'message')
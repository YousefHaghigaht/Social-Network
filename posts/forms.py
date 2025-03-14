from django import forms
from .models import Post,Comment


class PostCreateUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
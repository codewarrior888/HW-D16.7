from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'title': forms.TextInput(attrs={'size': '100'})}
        fields = ['title', 'content', 'category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 10:
            raise ValidationError({
                "title": "Title should contain at least 10 characters.",
            })

        content = cleaned_data.get("content")
        if content == title:
            raise ValidationError({
                "Title and content should be different.",
            })

        return cleaned_data

    def clean_name(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError({
                "Title should start with an uppercase letter.",
            })
        return title


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content']
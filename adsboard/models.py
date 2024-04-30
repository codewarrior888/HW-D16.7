from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, help_text="Category name")

    def __str__(self):
        return self.name
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=128)
    content = RichTextField(blank=True, null=True)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='categorys')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    @property
    def preview(self):
        words = self.content.split()
        preview_text = ' '.join(words[:20])
        if len(words) > 20:
            preview_text += '...'
        return preview_text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering=['-post_time']

    def __str__(self):
        return 'Comment by {}'.format(self.author)
    
    def get_absolute_url(self):
        return f'{self.pk}'
    

class OTPCode(models.Model):
    code = models.BigIntegerField()
    related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
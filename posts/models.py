from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return f'{self.user} - {self.slug}'
    
    def get_absolute_url(self):
        return reverse('posts:detail',args=[self.id])
    
    def like_count(self):
        return self.plikes.count()
    
    def can_like(self,user):
        likes = user.likes.filter(post=self)
        if likes.exists():
            return True
        return False
        
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body = models.CharField(max_length=400)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,related_name='rcomments',blank=True,null=True)
    is_reply = models.BooleanField(default=False) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.post}'
    
class Vote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='plikes')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} liked {self.post}'

    
from django.db import models
from django.contrib.auth.models import User

class Relation(models.Model):
    user_from = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    user_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_from} following {self.user_to}'
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField(default=0)





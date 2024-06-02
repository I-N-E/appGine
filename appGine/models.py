from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DataUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    phone = models.CharField(max_length=20,null=True,blank=True)
    birthday = models.DateField(null=True,blank=True)
    sex = models.CharField(max_length=10,null=True,blank=True )
    location = models.CharField(max_length=255,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    picture = models.ImageField(default='media/user.png',upload_to='media',null=True,blank=True)
    
    def __str__(self) -> str:
        return f'Data User : {self.user}'

class BlockPost(models.Model):
    user_post = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    datetime = models.DateTimeField(auto_now_add=True,null=False)
    title = models.CharField(max_length=100,null=False,blank=False)
    post = models.TextField(null=False,blank=False)
    good_post = models.IntegerField(default=0,null=True,blank=True)
    picture_post = models.ImageField(upload_to='media_post',null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.user_post} : {self.title}'
    
class CommentPost(models.Model):
    position_post = models.ForeignKey(BlockPost,on_delete=models.CASCADE,null=False)
    user_comment = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    datetime = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False,blank=False)
    good_comment = models.IntegerField(default=0,null=True,blank=True)
    picture_comment = models.ImageField(upload_to='media_comment',null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.position_post} : {self.user_comment}'
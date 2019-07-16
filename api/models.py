from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Like(models.Model):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete="CASCADE")
    content_type = models.ForeignKey(ContentType, on_delete="CASCADE")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Post(models.Model):
    user=models.ForeignKey(User,on_delete="CASCADE",null=True)
    title=models.CharField(max_length=300)
    body=models.TextField()
    pub_date=models.DateTimeField(auto_now_add=True)
    likes=GenericRelation(Like)

    def __str__(self):
        return self.title
    
    @property
    def total_likes(self):
        return self.likes.count()

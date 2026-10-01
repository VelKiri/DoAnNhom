from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from User.models import CustomUser
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    content = RichTextUploadingField()
    published_at= models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='blog/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # serializers.py

    class Meta:
        db_table = "blog"
    def str(self):
        return self.title

class Rate(models.Model):
    rate = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table="rate"
        unique_together = ('user','blog')

    def str(self):
        return str(self.rate)

class Comment(models.Model):
    comment = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='children')
    def str(self):
        return self.comment

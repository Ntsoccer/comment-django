from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.PROTECT,blank=False)
    title=models.CharField('タイトル',max_length=100)
    content=models.TextField('内容',null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

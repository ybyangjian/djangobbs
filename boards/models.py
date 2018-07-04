from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    '''
    论坛版块
    '''
    #unique=True设置name的唯一性
    name = models.CharField(verbose_name='版块名称',max_length=30,unique=True)
    description = models.CharField(verbose_name='版块介绍',max_length=100)

    def __str__(self):
        return self.name

class Topic(models.Model):
    '''
    主题
    '''
    subject = models.CharField(verbose_name='主题内容',max_length=255)
    last_updated = models.DateTimeField(name='话题排序',auto_now_add=True)
    board = models.ForeignKey(Board,related_name='topics',on_delete=models.CASCADE)
    starter = models.ForeignKey(User,related_name='topics',on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    message = models.TextField(verbose_name='回复内容',max_length=4000)
    topic = models.ForeignKey(Topic,verbose_name='主题',related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='排序')
    updated_at = models.DateTimeField(null=True,verbose_name='更新')
    created_by = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User,related_name='+',null=True,on_delete=models.CASCADE)

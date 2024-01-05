# coding=utf8
import base64

from django.db import models

# 用户的微信相关信息
class userWechat(models.Model):

    uid = models.CharField(max_length=32,unique=True,help_text='唯一用户编号')
    openid = models.CharField(max_length=64,help_text='用户openid')
    unionid = models.CharField(max_length=64,help_text='用户unionid')
    avatar = models.ImageField(upload_to='wechat_avatar/',blank=True,null=True)

    class Meta:

        app_label = 'iching_main'
        db_table = 'user_wechat'
# coding=utf8

from django.db import models

import time

# 用户基本信息
class userInfo(models.Model):

    uid = models.CharField(max_length=32,unique=True,help_text='唯一用户编号')
    user_name = models.CharField(max_length=32,default=f'用户{int(time.time())}',help_text='用户昵称')
    user_email = models.EmailField(help_text='用户邮箱')
    user_phone = models.CharField(max_length=16,default='0',help_text='手机号码')

    class Meta:

        app_label = 'iching_main'
        db_table = 'user_info'
# coding=utf8

from django.db import models
from django.utils import timezone

# token相关信息
class wechatTokenRecord(models.Model):

    access_token = models.CharField(max_length=None,help_text='access')
    expires_in = models.IntegerField(default=0,help_text='expires_in')
    update_dt = models.DateTimeField(default=timezone.now,auto_now=False,auto_now_add=False,help_text='创建时间')
    access_status = models.IntegerField(default=0,help_text='access_status')

    class Meta:

        app_label = 'iching_main'
        db_table = 'wechat_token_record'
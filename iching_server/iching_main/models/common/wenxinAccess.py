# coding=utf8

from django.db import models
from django.utils import timezone

# token相关信息
class baiduTokenRecord(models.Model):

    refresh_token = models.CharField(max_length=None,help_text='refresh')
    access_token = models.CharField(max_length=None,help_text='access')
    session_key = models.CharField(max_length=None,help_text='session_key')
    session_secret = models.CharField(max_length=None,help_text='session_secret')
    expires_in = models.IntegerField(default=0,help_text='expires')
    scope_area = models.CharField(max_length=None,help_text='scope')
    update_dt = models.DateTimeField(default=timezone.now,auto_now=False,auto_now_add=False,help_text='创建时间')
    access_status = models.IntegerField(default=0,help_text='access_status')

    class Meta:

        app_label = 'iching_main'
        db_table = 'baidu_token_record'

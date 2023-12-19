# coding=utf8

from django.db import models
from django.contrib.postgres.fields import ArrayField

class guaRecord(models.Model):

    openid = models.CharField(max_length=64,help_text='用户openid')
    yaos = ArrayField(models.IntegerField())
    user_gua = models.CharField(max_length=8,help_text='卦象')
    user_ques = models.CharField(max_length=None,help_text='问题')
    ai_answer = models.CharField(max_length=None,help_text='解语')
    rec_dt = models.DateTimeField(auto_now=False,auto_now_add=False,help_text='创建时间')
    total_tokens = models.IntegerField(default=0,help_text='token合计')
    prompt_tokens = models.IntegerField(default=0,help_text='参数token')
    completion_tokens = models.IntegerField(default=0,help_text='完善token')

    class Meta:

        app_label = 'iching_main'
        db_table = 'gua_record'
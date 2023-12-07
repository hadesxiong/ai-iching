# coding=utf8

from django.db import models

# 卦象基本信息
class guaInfo(models.Model):

    gua_symbol = models.CharField(max_length=12,help_text='卦象')
    gua_name = models.CharField(max_length=12,help_text='卦名')
    gua_desc= models.CharField(max_length=128,help_text='批语')
    gua_sentence = models.CharField(max_length=256,help_text='卦辞')

    class Meta:

        app_label = 'iching_main'
        db_table = 'gua_info'
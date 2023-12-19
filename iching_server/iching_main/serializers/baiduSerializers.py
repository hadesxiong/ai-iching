# coding=utf8
from rest_framework import serializers
from iching_main.models.common.wenxinAccess import baiduTokenRecord

# 序列化
class BaiduTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = baiduTokenRecord
        fields = ('access_token','expires_in','update_dt')
# coding=utf8
from rest_framework import serializers
from iching_main.models.common.wechatAccess import wechatTokenRecord

# 序列化
class WeChatTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = wechatTokenRecord
        fields = ('access_token','expires_in','update_dt')
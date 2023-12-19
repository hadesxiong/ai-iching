# coding=utf8

from rest_framework import serializers

from iching_main.models.gua.guaInfo import guaInfo
from iching_main.models.gua.guaRecord import guaRecord

# 序列化
class GuaInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = guaInfo
        fields = ('gua_name','gua_desc','gua_sentence')

class GuaRecSerializer(serializers.ModelSerializer):

    class Meta:
        model = guaRecord
        fields = ('id','yaos','user_gua','user_ques','ai_answer','rec_dt')
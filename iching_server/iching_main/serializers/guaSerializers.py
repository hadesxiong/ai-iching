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

    gua_name = serializers.SerializerMethodField()
    gua_desc = serializers.SerializerMethodField()
    gua_time = serializers.SerializerMethodField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        gua_queryset = guaInfo.objects.all().values('gua_name','gua_symbol','gua_desc')
        self.gua_dict = {item['gua_symbol']:{'gua_name':item['gua_name'],'gua_desc':item['gua_desc']} for item in gua_queryset}

    def get_gua_name(self,obj):
        return self.gua_dict[obj.user_gua]['gua_name']
    
    def get_gua_desc(self,obj):
        return self.gua_dict[obj.user_gua]['gua_desc']
    
    def get_gua_time(self,obj):
        return f'{obj.rec_dt.year}.{obj.rec_dt.month:02d}.{obj.rec_dt.day:02d}'

    class Meta:
        model = guaRecord
        fields = ('id','yaos','user_gua','user_ques','ai_answer','gua_time','gua_name','gua_desc')
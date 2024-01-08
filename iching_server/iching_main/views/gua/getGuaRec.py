# coding=utf8

from rest_framework.decorators import api_view,permission_classes
from django.http.response import JsonResponse
from django.core.paginator import Paginator

from dotenv import load_dotenv

from iching_main.models.gua.guaRecord import guaRecord
from iching_main.serializers.guaSerializers import GuaRecSerializer
from iching_main.utils.customPermissions import NormalUserPermission

import math

@api_view(['GET'])
@permission_classes([NormalUserPermission])
def getGuaRec(request):

    user_openid = request.headers.get('Userid')
    rec_id = request.query_params.get('target','all')
    page_num = int(request.query_params.get('page',1))

    if rec_id == 'all':
        gua_rec = guaRecord.objects.filter(openid=user_openid).order_by('-rec_dt')
        # 分页
        gua_paginator = Paginator(gua_rec,20)
        page_max = math.ceil(len(gua_rec)/20)

        if page_num <= page_max:
            each_gua_rec = gua_paginator.page(page_num)
            each_gua_rec_s = GuaRecSerializer(each_gua_rec,many=True)
            re_msg = {'code':0,'list':each_gua_rec_s.data,'has_next':page_num<page_max}

        else:
            re_msg = {'code':1,'msg':'err range.'}
            
    else:
        gua_rec = guaRecord.objects.filter(openid=user_openid,id=rec_id)
        if len(gua_rec) !=0:
            gua_rec = GuaRecSerializer(gua_rec,many=True).data[0]
            re_msg = {'code':0,'item':gua_rec}
        else:
            re_msg = {'code':1,'msg':'error_params.'}

    return JsonResponse(re_msg,safe=False)
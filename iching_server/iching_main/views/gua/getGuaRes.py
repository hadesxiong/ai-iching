# coding=utf8
import os

from rest_framework.decorators import api_view,permission_classes
from django.http.response import JsonResponse

from iching_main.models.common.wenxinAccess import baiduTokenRecord
from iching_main.serializers.baiduSerializers import BaiduTokenSerializer
from iching_main.utils.customPermissions import NormalUserPermission, UsagePermission
from iching_main.utils.getGuaRelated import get_3_coins,get_gua_xiang,get_yin_yang,format_coin_result

from dotenv import load_dotenv

# 读取配置
load_dotenv()

@api_view(['GET'])
def getGuaRes(request):

    coin_results = []

    first_yao = []
    for i in range(3):
        coin_res = get_3_coins()
        first_yao.append(get_yin_yang(coin_res))
        coin_results.append(format_coin_result(coin_res,i))
    first_gua = get_gua_xiang(first_yao)

    second_yao = []
    for i in range(3,6):
        coin_res = get_3_coins()
        second_yao.append(get_yin_yang(coin_res))
        coin_results.append(format_coin_result(coin_res,i))
    second_gua = get_gua_xiang(second_yao)
    
    re_msg = {'coin_res':coin_results,'yao':[first_yao,second_yao],'first_gua':first_gua,'second_gua':second_gua,'guaxiang':f'{first_gua}{second_gua}'}

    return JsonResponse(re_msg,safe=False)

@api_view('POST')
@permission_classes([NormalUserPermission,UsagePermission])
def getLiuYaoResult(request):

    # 解析bodydata
    body_data = {
        'questions': request.data.get('q',None)
    }

    if None in body_data.values():
        re_msg = {'code':0,'msg':'err params.'}

    else:
        # 找出百度token
        baidu_token = baiduTokenRecord.objects.filter(access_status=1)
        baidu_token_item = BaiduTokenSerializer(baidu_token,many=True)[0]
        

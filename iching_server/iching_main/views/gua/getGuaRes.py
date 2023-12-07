# coding=utf8

from rest_framework.decorators import api_view

from django.http.response import JsonResponse

from iching_main.utils.getGuaRelated import get_3_coins,get_gua_xiang,get_yin_yang,format_coin_result

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
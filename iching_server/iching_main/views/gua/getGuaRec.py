# coding=utf8

from rest_framework.decorators import api_view,permission_classes
from django.http.response import JsonResponse

from dotenv import load_dotenv

from iching_main.models.gua.guaRecord import guaRecord
from iching_main.serializers.guaSerializers import GuaRecSerializer
from iching_main.utils.customPermissions import NormalUserPermission

@api_view(['GET'])
@permission_classes([NormalUserPermission])
def getGuaRec(request):

    user_openid = request.headers.get('Userid')
    rec_id = request.query_params.get('target','all')

    if rec_id == 'all':
        gua_rec = guaRecord.objects.filter(openid=user_openid)
        gua_rec = GuaRecSerializer(gua_rec,many=True).data
        
        re_msg = {'code':0,'list': gua_rec}

    else:
        gua_rec = guaRecord.objects.filter(openid=user_openid,id=rec_id)
        if len(gua_rec) !=0:
            gua_rec = GuaRecSerializer(gua_rec,many=True).data[0]
            re_msg = {'code':0,'item':gua_rec}
        else:
            re_msg = {'code':1,'msg':'error_params.'}

    return JsonResponse(re_msg,safe=False)
# coding=utf8
import requests,os,json,datetime,uuid

from rest_framework.decorators import api_view
from django.http.response import JsonResponse

from dotenv import load_dotenv

from iching_main.models.common.wechatAccess import wechatTokenRecord
from iching_main.models.user.userWechat import userWechat
from iching_main.models.user.userMain import userMain
from iching_main.serializers.wechatSerializers import WeChatTokenSerializer
from iching_main.utils.getWeChatToken import updateWeChatToken

# 读取配置
load_dotenv()

@api_view(['GET'])
def userLogin(request):

    request_params = {
        'code': request.query_params.get('code',None)
    }

    if None in request_params.values():
        re_msg = {'code':1,'msg':'error code'}

    else:
        # 找出微信token
        wechat_token = wechatTokenRecord.objects.filter(access_status=1)
        if len(wechat_token) <1:
            updateWeChatToken()
            wechat_token = wechatTokenRecord.objects.filter(access_status=1)
        
        wechat_token_item = WeChatTokenSerializer(wechat_token,many=True).data[0]

        # 判断token有效期,超过了重新请求一条token写入数据库
        update_dt = int(datetime.datetime.strptime(wechat_token_item['update_dt'],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        token_expire_dt = update_dt + wechat_token_item['expires_in']
        if token_expire_dt < int(datetime.datetime.now().timestamp()):
            updateWeChatToken()
            wechat_token = wechatTokenRecord.objects.filter(access_status=1)
            wechat_token_item = WeChatTokenSerializer(wechat_token,many=True).data[0]
        
        request_params = {
            'appid': os.getenv('WEAPP_APPID'),
            'secret': os.getenv('WEAPP_APPSECRET'),
            'js_code': request_params['code'],
            'grant_type': 'authorization_code'
        }

        code_res = requests.request('GET',os.getenv('WEAPP_JSCODE_URL'),params=request_params)

        if 'errcode' in json.loads(code_res.text).values():
            re_msg = {'code':1,'msg':'err code.'}
        else:
            openid = json.loads(code_res.text)['openid']
            unionid = json.loads(code_res.text)['unionid']

            # 判断用户是否存在
            try:
                userWechat.objects.get(openid=openid)
            except userWechat.DoesNotExist:
                uid = str(uuid.uuid5(uuid.NAMESPACE_DNS,'bierman')).replace('-','')
                userWechat.objects.create(
                    uid=uid,openid=openid,unionid=unionid
                )
                userMain.objects.create(
                    uid=uid,user_state=1,user_create=datetime.datetime.now(),user_character=1
                )

            re_msg = {'code':0,'openid':openid,'unionid':unionid}

    return JsonResponse(re_msg,safe=False)
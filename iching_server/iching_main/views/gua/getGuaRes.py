# coding=utf8
import os,requests,datetime,json,re

from rest_framework.decorators import api_view,permission_classes
from django.http.response import JsonResponse

from dotenv import load_dotenv

from iching_main.models.common.wenxinAccess import baiduTokenRecord
from iching_main.models.gua.guaRecord import guaRecord
from iching_main.models.gua.guaInfo import guaInfo
from iching_main.serializers.baiduSerializers import BaiduTokenSerializer
from iching_main.serializers.guaSerializers import GuaInfoSerializer
from iching_main.utils.customPermissions import NormalUserPermission, UsagePermission
from iching_main.utils.getGuaRelated import get_gua_xiang,get_yin_yang
from iching_main.utils.getBaiduToken import updateBaiduToken

# 读取配置
load_dotenv()

# 配置默认msg
prompt_begin = '''你是一位出自中华六爻世家的卜卦专家，你的任务是根据卜卦者的问题和得到的卦象，为他们提供有益的建议。
                你的解答应基于卦象的理解，同时也要尽可能地展现出乐观和积极的态度，引导卜卦者朝着积极的方向发展。问题是：'''

@api_view(['GET'])
@permission_classes([NormalUserPermission,UsagePermission])
def getGuaRes(request):

    request_params = {
        'coin_res': request.query_params.get('coin',None)
    }

    if None in request_params.values():
        re_msg = {'code':1,'msg':'err params.'}

    elif re.match("^[01]+$",request_params['coin_res']) is None:
        re_msg = {'code':1,'msg':'err coin_res.'}
    
    elif len(request_params['coin_res']) != 18:
        re_msg = {'code':1,'msg':'err coin_res length.'}

    else:
        coin_result = [char for char in request_params['coin_res']]
        coin_result = [[int(num) for num in coin_result[i:i+3]] for i in range(0,len(coin_result),3)]

        first_yao = [get_yin_yang(each_res) for each_res in coin_result[0:3]]
        second_yao = [get_yin_yang(each_res) for each_res in coin_result[3:6]]

        re_msg = {
            'code':0,
            'first_yao':first_yao,
            'second_yao':second_yao,
            'first_gua':get_gua_xiang(first_yao),
            'second_gua': get_gua_xiang(second_yao),
            'gua_symbol': get_gua_xiang(second_yao) + get_gua_xiang(first_yao)
        }

    return JsonResponse(re_msg,safe=False)

@api_view(['POST'])
@permission_classes([NormalUserPermission,UsagePermission])
def getLiuYaoRes(request):

    # 解析bodydata
    body_data = {
        'questions': request.data.get('q',None),
        'yao_res': request.data.get('yao',None),
        'gua_symbol': request.data.get('gua',None)
    }

    user_openid = request.headers.get('Userid')

    if None in body_data.values():
        re_msg = {'code':0,'msg':'err params.'}

    else:
        # 找出百度token
        baidu_token = baiduTokenRecord.objects.filter(access_status=1)
        if len(baidu_token)<1:
            updateBaiduToken()
            baidu_token = baiduTokenRecord.objects.filter(access_status=1)
        
        baidu_token_item = BaiduTokenSerializer(baidu_token,many=True).data[0]

        # 判断token有效期是否超过，超过了重新请求一条token写入数据库
        update_dt = int(datetime.datetime.strptime(baidu_token_item['update_dt'],"%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
        token_expire_dt = update_dt + baidu_token_item['expires_in']
        if token_expire_dt < int(datetime.datetime.now().timestamp()):
            updateBaiduToken()
            baidu_token = baiduTokenRecord.objects.filter(access_status=1)
            baidu_token_item = BaiduTokenSerializer(baidu_token,many=True)[0]

        # 查找其他卦相关信息
        gua_item = guaInfo.objects.filter(gua_symbol=body_data['gua_symbol'])
        if len(gua_item) < 1:
            re_msg = {'code':1,'err_msg':'error params.'}
        else:
            gua_item = GuaInfoSerializer(gua_item,many=True).data[0]
        
            # 拼接参数
            request_headers = {
                'Content-Type':'application/json',
                'Accept':'application/json'
            }
            request_params = {'access_token': baidu_token_item['access_token']}
            request_data = {
                'messages':[{
                    'role':'user',
                    'content':(
                        f'{prompt_begin}{body_data["questions"]};'
                        f'六爻结果是:{body_data["gua_symbol"]};'
                        f'卦名为:{gua_item["gua_name"]},{gua_item["gua_desc"]};'
                        f'卦辞为:{gua_item["gua_sentence"]}'
                    )
                }]
            }
            print(request_data)
            yao_res = requests.request('POST',os.getenv('ERNIE_BOT_TURBO'),headers=request_headers,
                                    params=request_params,data=json.dumps(request_data))

            # 补充判断逻辑
            if 'error_code' in json.loads(yao_res.text).keys():
                re_msg = {'code':1,'msg':'error params'}
            else:
                ai_answer = json.loads(yao_res.text)['result']
                completion_tokens = json.loads(yao_res.text)['usage']['completion_tokens']
                prompt_tokens = json.loads(yao_res.text)['usage']['prompt_tokens']
                total_tokens = json.loads(yao_res.text)['usage']['total_tokens']

                # 调用结果写入记录
                yao_item = [int(char) for char in body_data['yao_res']]
                guaRecord.objects.create(
                    openid=user_openid,yaos=yao_item,user_gua=body_data['gua_symbol'],user_ques=body_data['questions'],
                    ai_answer=ai_answer,
                    rec_dt=datetime.datetime.fromtimestamp(json.loads(yao_res.text)['created']),
                    completion_tokens=completion_tokens,prompt_tokens=prompt_tokens,total_tokens=total_tokens
                )

                re_msg = {'code':0,'result':json.loads(yao_res.text)['result']}

    return JsonResponse(re_msg,safe=False)
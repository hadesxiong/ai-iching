# coding=utf8

import os,requests,json,datetime
from dotenv import load_dotenv

from iching_main.models.common.wechatAccess import wechatTokenRecord

# 读取配置
load_dotenv()

def updateWeChatToken():

    request_params = {
        'grant_type':'client_credential',
        'appid': os.getenv('WEAPP_APPID'),
        'secret': os.getenv('WEAPP_APPSECRET')
    }

    # 请求weapptoken
    weapp_res = requests.request('GET',os.getenv('WEAPP_TOKEN_URL'),params=request_params)

    res_data = json.loads(weapp_res.text)

    if 'errcode' in res_data.keys():
        # 待补充通知逻辑
        # 参照官方文档，出现errorcode时，同步会返回errmsg
        pass

    else:
        # 更新所有token_record的状态为0
        wechatTokenRecord.objects.filter(access_status=1).update(access_status=0)

        # 插入一条记录,access_status设置为1
        wechatTokenRecord.objects.create(
            access_token=res_data['access_token'],expires_in=res_data['expires_in'],
            update_dt=datetime.datetime.now(),access_status=1
        )

    # 待补充日志逻辑
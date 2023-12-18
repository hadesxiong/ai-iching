# coding=utf8

import os,requests,psycopg2,json,datetime
from dotenv import load_dotenv

from iching_main.models.common.wenxinAccess import baiduTokenRecord

# 读取配置
load_dotenv()

def updateBaiduToken():

    request_headers = {
        'Content-Type':'application/json',
        'Accept':'application/json'
    }

    request_params = {
        'grant_type':'client_credentials',
        'client_id': os.getenv('BAIDU_CLIENT_ID'),
        'client_secret': os.getenv('BAIDU_CLIENT_SECRET')
    }

    # 请求百度token
    baidu_res = requests.request('POST',os.getenv('BAIDU_TOKEN_URL'),
                                 headers=request_headers,params=request_params)
    
    res_data = json.loads(baidu_res.text)

    if 'error' in res_data.keys():
        # 待补充通知逻辑
        # 参照官方文档，出现errors时会同步返回error_description
        pass
    
    else:
        # 非orm操作
        # # 创建postgresql链接
        # psql_conn = psycopg2.connect(
        #     host=os.getenv('POSTGRES_HOST'),port=os.getenv('POSTGRES_PORT'),
        #     database=os.getenv('POSTGRES_DB'),user='postgres',
        #     password=os.getenv('POSTGRES_PW'),options="-c search_path=main_server"
        # )
        # psql_cursor = psql_conn.cursor()

        # # 更新所有token_record的状态为0
        # status_sql = "UPDATE BAIDU_TOKEN_RECORD SET ACCESS_STATUS=0"
        # psql_cursor.execute(status_sql)
        
        # # 插入一条新纪录，status设置为1
        # insert_sql = "INSERT INTO BAIDU_TOKEN_RECORD \
        #         (REFRESH_TOKEN,ACCESS_TOKEN,SESSION_KEY,SESSION_SECRET, \
        #         EXPIRES_IN,SCOPE_AREA,ACCESS_STATUS,UPDATE_DT) VALUES \
        #         (%s,%s,%s,%s,%s,%s,%s,%s)"
        # insert_data = (
        #     res_data.get('refresh_token'),res_data.get('access_token'),res_data.get('session_key'),res_data.get('session_secret'),
        #     res_data.get('expires_in'),res_data.get('scope'),1,datetime.datetime.now()
        # )
        # psql_cursor.execute(insert_sql,insert_data)
        # # 提交
        # psql_conn.commit()
        # # 关闭
        # psql_cursor.close()
        # psql_conn.close()

        # orm操作
        # 更新所有token_record的状态为0
        baiduTokenRecord.objects.filter(access_status=1).update(access_status=0)

        # 插入一条记录,access_status设置为1
        baiduTokenRecord.objects.create(
            refresh_token=res_data.get('refresh_token'),access_token=res_data.get('access_token'),
            session_key=res_data.get('session_key'),session_secret=res_data.get('session_secret'),
            expires_in=res_data.get('expires_in'),scope_area=res_data.get('scope'),update_dt=datetime.datetime.now(),
            access_status=1
        )

    # 待补充日志逻辑
    
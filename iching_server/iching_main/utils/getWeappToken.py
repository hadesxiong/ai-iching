# coding=utf8

import os,requests,psycopg2,json,datetime
from dotenv import load_dotenv

# 读取配置
load_dotenv()

def updateWeappToken():

    request_params = {
        'grant_type':'client_credential',
        'appid': os.getenv('WEAPP_APPID'),
        'secret': os.getenv('WEAPP_APPSECRET')
    }

    # 请求weapptoken
    weapp_res = requests.request('GET',os.getenv('WEAPP_TOKEN_URL'),params=request_params)

    res_data = json.loads(weapp_res)

    if 'errcode' in res_data.keys():
        # 待补充通知逻辑
        # 参照官方文档，出现errorcode时，同步会返回errmsg
        pass

    else:
        # 创建postgresql链接
        psql_conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB'),user='postgres',
            password=os.getenv('POSTGRES_PW'),options="-c search_path=main_server"
        )
        psql_cursor = psql_conn.cursor()

        # 更新所有token_record状态为0
        status_sql = "UPDATE WECHAT_TOKEN_RECORD SET ACCESS_STATUS=0"
        psql_cursor.execute(status_sql)

        # 插入一条记录
        insert_sql = "INSERT INTO WECHAT_TOKEN_RECORD \
                (ACCESS_TOKEN,EXPIRES_IN,UPDATE_DT,ACCESS_STATUS) \
                VALUES (%s,%s,%s,%s)"
        insert_data = (res_data.get('access_token'),res_data.get('expires_in'),
                       datetime.datetime.now(),1)
        psql_cursor.execute(insert_sql,insert_data)
        # 提交
        psql_conn.commit()
        # 关闭
        psql_cursor.close()
        psql_conn.close()

    # 待补充日志逻辑
# coding=utf8

from rest_framework.permissions import BasePermission
from iching_main.models.user.userWechat import userWechat
from iching_main.models.gua.guaRecord import guaRecord

class NormalUserPermission(BasePermission):

    # 查询逻辑：用户是否已经注册，如果不注册则不展示
    def has_permission(self,request,view):
        openid = request.headers.get('user_id')
        # 待补充解密逻辑
        
        if openid:
            try:
                user_wechat = userWechat.objects.get(openid=openid)
                return True
            except userWechat.DoesNotExist:
                return False
            
        return False
    
class UsagePermission(BasePermission):

    # 查询逻辑：用户是否在当日还剩余使用次数
    def has_Permission(self,request,view):
        openid = request.headers.get('user_id')
        # 待补充解密逻辑

        if openid:
            try:
                today_usage = guaRecord.objects.filter(openid=openid)
                if len(today_usage) >=2:
                    return False
                else:
                    return True
            except:
                return False

        return False
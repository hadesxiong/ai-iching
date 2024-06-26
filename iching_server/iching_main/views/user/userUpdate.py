# coding=utf8
from rest_framework.decorators import api_view,permission_classes
from django.core.files.storage import default_storage
from django.conf import settings
from django.http.response import JsonResponse

from iching_main.models.user.userInfo import userInfo
from iching_main.models.user.userWechat import userWechat
from iching_main.models.user.userMain import userMain
from iching_main.utils.customPermissions import NormalUserPermission

@api_view(['POST'])
@permission_classes([NormalUserPermission])
def userUpdate(request):

    body_data = {
        'user_info': request.data.get('info',None),
        'type': request.data.get('type',None)
    }
    openid = request.headers.get('Userid')
    uid = userWechat.objects.get(openid=openid).uid

    if None in body_data.values():
        re_msg = {'code':1,'msg':'error params'}

    elif body_data['type'] == 'main':
        user_character = body_data['user_info'].get('character',None)
        if user_character:
            userMain.objects.filter(uid=uid).update(user_character=int(user_character))           
            re_msg = {'code':0,'msg':'update success.'}
        else:
            re_msg = {'code':1,'msg':'error params.'}

    elif body_data['type'] == 'info':
        user_obj = userInfo.objects.get(uid=uid)
        keys_to_check = ['name','email','phone']
        for key in keys_to_check:
            if key in body_data['user_info']:
                setattr(user_obj,f'user_{key}',body_data['user_info'][key])
        user_obj.save()
        re_msg = {'code':0,'msg':'update success'}

    else:
        re_msg = {'code':1,'msg':'error params.'}

    return JsonResponse(re_msg,safe=False)


@api_view(['POST'])
@permission_classes([NormalUserPermission])
def avatarUpdate(request):

    avatar_file = request.FILES.get('avatar')
    openid = request.headers.get('Userid')

    if avatar_file and openid:

        try:
            user_wechat = userWechat.objects.get(openid=openid)
            avatar_path = default_storage.save('images/'+avatar_file.name,avatar_file)

            # 构建url地址
            avatar_url = settings.MEDIA_URL + avatar_path
            user_wechat.avatar = avatar_path
            user_wechat.save()

            re_msg = {'code':0,'image_url':avatar_url}

        except userWechat.DoesNotExist:
            re_msg = {'code':1,'msg':'no user.'}

    else:
        re_msg = {'code':1,'msg':'no user'}

    return JsonResponse(re_msg,safe=False)
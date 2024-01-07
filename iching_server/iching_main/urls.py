# coding=utf8

from django.urls import path
from iching_main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # user
    path('api/user/userLogin',views.userLogin),
    path('api/user/userUpdate',views.userUpdate),
    path('api/user/avatarUpdate',views.avatarUpdate),

    #gua
    path('api/liuyao/getGuaRes',views.getGuaRes),
    path('api/liuyao/getLiuYaoRes',views.getLiuYaoRes),
    path('api/liuyao/getGuaRec',views.getGuaRec)
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
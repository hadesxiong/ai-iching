# coding=utf8

from django.urls import path
from iching_main import views

urlpatterns = [
    # user
    path('api/user/userLogin',views.userLogin),

    #gua
    path('api/liuyao/getGuaRes',views.getGuaRes),
    path('api/liuyao/getLiuYaoRes',views.getLiuYaoRes),
    path('api/liuyao/getGuaRec',views.getGuaRec)
]
# coding=utf8

from django.urls import path
from iching_main import views

urlpatterns = [
    
    #gua
    path('api/liuyao/getGuaRes',views.getGuaRes)

]
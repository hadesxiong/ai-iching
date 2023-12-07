# coding=utf8

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone

import uuid,time

# 自定义用户管理
class CustomUserManager(BaseUserManager):

    def createUser(self):

        new_uuid = str(uuid.uuid4()).replace('-','')
        user = self.model(uid = new_uuid,user_create = timezone.now())
        user.save()
        return user

# 用户主表
class userMain(AbstractBaseUser):

    uid = models.CharField(max_length=32,unique=True,help_text='唯一用户编号')
    user_state = models.IntegerField(default=1,help_text='用户状态')
    user_create= models.DateTimeField(auto_now_add=True,auto_now=False,help_text='创建时间')
    user_character = models.IntegerField(default=1,help_text='用户角色')

    # 删除password/last_login
    password = None
    last_login = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = []

    class Meta:

        app_label = 'iching_main'
        db_table = 'user_main'
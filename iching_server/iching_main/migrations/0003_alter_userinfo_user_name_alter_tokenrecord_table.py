# Generated by Django 4.2.7 on 2023-12-12 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iching_main', '0002_tokenrecord_alter_userinfo_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_name',
            field=models.CharField(default='用户1702352589', help_text='用户昵称', max_length=32),
        ),
        migrations.AlterModelTable(
            name='tokenrecord',
            table='baidu_token_record',
        ),
    ]

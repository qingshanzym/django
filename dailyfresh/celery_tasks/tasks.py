# coding=utf-8
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from celery import Celery

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "dailyfresh.settings"
# 放到Celery服务器上时添加的代码
import django
django.setup()

app=Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/5')

@app.task
def send_user_active(id, email):
    # 将账号信息进行加密
    serializer = Serializer(settings.SECRET_KEY, 60 * 60 * 2)
    value = serializer.dumps({'id': id})  # 返回bytes
    value = value.decode()  # 转成字符串，用于拼接地址

    # 向用户发送邮件
    # msg='<a href="http://127.0.0.1:8000/user/active/%d">点击激活</a>'%user.id
    msg = '<a href="http://127.0.0.1:8000/user/active/%s">点击激活</a>' % value
    send_mail('天天生鲜账户激活', '', settings.EMAIL_FROM, [email], html_message=msg)

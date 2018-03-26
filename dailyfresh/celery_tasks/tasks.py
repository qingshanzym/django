# coding=utf-8
# django内核中邮件内核。————发送邮件。
from django.core.mail import send_mail
# 导入django系统配置。里面含有关于发送邮件设置的常规配置。
from django.conf import settings
# 加密需要。itsdangerous是基于django安全签名的基础上封装的。SignatureExpired是相关异常。
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
# 导入celery中的Celery类。创建加密对象。
from celery import Celery

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "dailyfresh.settings"
# 放到Celery服务器上时添加的代码
import django
django.setup()

# 第一个参数是tasks路径，第二个是指定中间人——用redis。
app=Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/5')

# 用装饰器来注册发送激活邮件的函数。此处要注意，要传两个参数，分别为要加密的id属性，和发送邮箱地址中的email。不能直接传user对象，不然会报错：object is not a serializer Json.
@app.task
def send_user_active(id, email):
    # 将账号信息进行加密,1、用密文加密 2、失效时间。
    serializer = Serializer(settings.SECRET_KEY, 60 * 60 * 2)
    # 加密。
    value = serializer.dumps({'id': id})  # 返回bytes
    # 把加密的字节流转成字符串。
    value = value.decode()  # 转成字符串，用于拼接地址

    # 向用户发送邮件
    # msg='<a href="http://127.0.0.1:8000/user/active/%d">点击激活</a>'%user.id
    msg = '<a href="http://127.0.0.1:8000/user/active/%s">点击激活</a>' % value
    # 此处的参数传递可点开源码看，认真写。
    send_mail('天天生鲜账户激活', '', settings.EMAIL_FROM, [email], html_message=msg)

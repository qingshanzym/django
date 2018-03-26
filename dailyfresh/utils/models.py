# coding=utf-8
from django.db import models

# 定义基类，在这里定义每个表的都会有的属性————创建时间和更新时间。
class BaseModel(models.Model):
    # 添加时间
    add_date = models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    # 最近修改时间
    update_date = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    # 逻辑删除
    isDelete = models.BooleanField(default=False,verbose_name='逻辑删除')
    # 把abstract的值改为Ture，则表示这个类为抽象基类。抽象基类是可以在不迁移这张抽象基类表的情况下，让其他继承了这个抽象基类的类拥有此基类的属性。
    class Meta:
        abstract=True

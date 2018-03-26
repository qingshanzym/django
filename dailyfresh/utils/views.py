# coding=utf-8
# 一般视图类
from django.views.generic import View
# 用户权限验证，这个装饰器login_required已经让django给我们封装好了
from django.contrib.auth.decorators import login_required


# 在django中对于类视图添加装饰器的方式
class LoginRequiredView(View):
    @classmethod
    def as_view(cls, **initkwargs):
        func = super().as_view(**initkwargs)
        return login_required(func)


# 多继承的方案，这是django推荐的给类视图添加装饰器的方式。
class LoginRequiredViewMixin(object):
    @classmethod
    # 重写as_view方法
    def as_view(cls, **initkwargs):
        func = super().as_view(**initkwargs)
        return login_required(func)
#     22行这行代码是装饰器的另外一种写法
# 一般我们是用语法糖的形式写，eg：f1 = log(f1)

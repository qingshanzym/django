# coding=utf-8
from django.conf.urls import url
from . import views
urlpatterns = [
    url('^test$',views.test),
    url('^$',views.index),
]
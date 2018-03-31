# coding=utf-8
from django.conf.urls import url
from . import views
urlpatterns = [
    url('^test$',views.test),
    url('^index$',views.index),
    url('^(\d+)', views.detail),
    url('^index_test$', views.index_test),
    url('^search/$', views.MySearchView.as_view())
]

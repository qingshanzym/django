# coding=utf-8
from django.conf.urls import url
from .views import *
urlpatterns = [
    # url('^register$',views.register),
    url('^register$',RegisterView.as_view()),
    url('^active/(.+)$',active),
    url('^exists$',exists),
    url('^login$',LoginView.as_view()),
]

# coding=utf-8
from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # url('^register$',views.register),
    url('^register$',RegisterView.as_view()),
    url('^active/(.+)$',active),
    url('^exists_user$',exists_user),
    url('^exists_email$', exists_email),
    url('^login$',LoginView.as_view()),
    url('^logout$', logout_user),
    url('^info$', info),
    url('^order$', order),
    url('^area$', area),
    url('^site$', SiteView.as_view())
]

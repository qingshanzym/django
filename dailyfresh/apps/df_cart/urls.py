from django.conf.urls import url
from .views import *
urlpatterns = [
    url('^add$', add),
    url('^$', index)
]
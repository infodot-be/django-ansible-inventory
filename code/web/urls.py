from django.conf.urls import url
from django.urls import path
from web import views

app_name = 'web'

urlpatterns = [
    url(r'^$', views.Indexview.as_view(), name='index'),
]

from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from api import views


"""
These are the auto generated routes by the REST API
"""
router = routers.DefaultRouter()
router.register(r'tenant', views.TenantViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'system', views.SystemViewSet)
# router.register(r'inventory/byname/(?P<name>[\w-]+)/$', views.YamlByName)
router.register(r'systemyaml', views.SystemYamlViewSet)
router.register(r'groupyaml', views.GroupYamlViewSet)
router.register(r'tenantyaml', views.TenantYamlViewSet)
# router.register(r'inventory/(?P<name>[\w-]+)/$', views.YamlByName)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('inventory/(?P<pk>[\\w-]+)/$', views.YamlDetail.as_view(), name='yaml-detail'),
    url('inventory/byname/(?P<name>[\\w-]+)/$', views.YamlByName.as_view(), name='yaml-list-name'),
]

from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import pagination, serializers, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.generics import (
    CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
)
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from .models import Tenant
# from .serializers import TenantSerializer, GroupSerializer, SystemSerializer
from .serializers import TenantSerializer


class ListViewPagination(pagination.PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BaseYamlDetail(RetrieveAPIView):
    serializer_class = TenantSerializer

    def get(self, request, *args, **kwargs):
        tenant = get_object_or_404(Tenant, pk=self.kwargs["id"])
        return tenant


class BaseYamlList(ListCreateAPIView):
    serializer_class = TenantSerializer
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (DjangoModelPermissions,)
    pagination_class = ListViewPagination
    queryset = Tenant.objects.all()

    # def get_queryset(self):
    #     tenants = get_list_or_404(models.Tenant)
    #     return tenants

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.generics import ListAPIView
from rest_framework import viewsets, generics
from .models import Tenant, Group, System, System_yaml, Group_yaml, Tenant_yaml
# from .serializers import TenantSerializer, GroupSerializer, SystemSerializer
from .serializers import (TenantSerializer, GroupSerializer, SystemSerializer,
                          SystemYamlSerializer, GroupYamlSerializer, TenantYamlSerializer)
from .generics import BaseYamlDetail, BaseYamlList
import json
import yaml
import logging
from .ansible_inventory import Ansible_inventory


class YamlDetail(APIView):
    """
    List All System from tenant by id
    """
    renderer_classes = [JSONRenderer]

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('YamlDetail')
        self.log = logger
        pass

    # @method_decorator(cache_page(60*60*2))
    def get(self, *args, **kwargs):
        tenant = self.kwargs['pk']
        try:
            self.tenant = get_object_or_404(Tenant, id=tenant)  # should be changed to group name
            inst = Ansible_inventory(tenant=self.tenant)
        except ValidationError:
            return HttpResponse(status=201)

        return Response(inst.get_inventory())


class YamlByName(APIView):
    renderer_classes = [JSONRenderer]
    queryset = Tenant.objects.all().order_by('name')

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('YamlByName')
        self.log = logger
        pass

    # @method_decorator(cache_page(60*60*2))
    # @action(detail=False)
    def get(self, *args, **kwargs):
        tenant = self.kwargs['name']
        try:
            self.tenant = get_object_or_404(Tenant, name=tenant)  # should be changed to group name
            inst = Ansible_inventory(tenant=self.tenant)
        except ValidationError:
            return HttpResponse(status=201)

        return Response(inst.get_inventory())


class TenantViewSet(viewsets.ModelViewSet):
    """
    List All Tenants via Generic View
    """
    queryset = Tenant.objects.all().order_by('name')
    serializer_class = TenantSerializer

    @action(detail=False)
    def get_by_name(self, request):
        """
        Get tenant information based on name search
        """
        tenant_name = self.request.query_params.get('name', None)
        tenants = Tenant.objects.filter(name=tenant_name).order_by('name')
        serializer = self.get_serializer(tenants, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    List All Groups via Generic View
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer

    @action(detail=False)
    def get_by_uuid(self, request):
        """
        Get Sytem information by id
        """
        group_id = self.request.query_params.get('id', None)

        groups = Group.objects.filter(id=group_id).order_by('name')
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_by_name(self, request):
        """
        Get Group information by name
        """
        group_name = self.request.query_params.get('name', None)
        groups = Group.objects.filter(name=group_name).order_by('name')
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data)


class SystemViewSet(viewsets.ModelViewSet):
    """
    List All Groups via Generic View
    """
    queryset = System.objects.all().order_by('name')
    serializer_class = SystemSerializer

    # def list(self, request, *args, **kwargs):
    #     return HttpResponse(status=404)

    @action(detail=False)
    def get_by_uuid(self, request):
        """
        Get system information by id
        """
        tenant = self.request.query_params.get('id', None)
        # systems = System.objects.filter(tenant=tenant).order_by('name')
        systems = System.objects.filter(tenant=tenant).order_by('name')
        serializer = self.get_serializer(systems, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_by_tenantname(self, request):
        """
        Get system information by name groupname
        """
        tenant = self.request.query_params.get('name', None)
        try:
            tenant_id = get_object_or_404(Tenant, name=tenant)
        except ValidationError:
            return HttpResponse(status=201)
        systems = System.objects.filter(tenant=tenant_id).order_by('name')
        serializer = self.get_serializer(systems, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_by_name(self, request):
        """
        Get system information by name
        """
        name = self.request.query_params.get('name', None)
        systems = System.objects.filter(name=name).order_by('name')
        serializer = self.get_serializer(systems, many=True)
        return Response(serializer.data)


class SystemViewSetByTenant(viewsets.ModelViewSet):
    """
    List All Groups via Generic View
    """
    renderer_classes = [JSONRenderer]
    queryset = System.objects.all().order_by('name')
    serializer_class = SystemSerializer

    @action(detail=False)
    def get_by_tenant(self, request):
        """
        """
        tenant = self.request.query_params.get('name', None)
        # systems = System.objects.filter(tenant=tenant).order_by('name')
        systems = System.objects.filter(tenant=tenant).order_by('name')
        serializer = self.get_serializer(systems, many=True)
        return Response(serializer.data)


class SystemYamlViewSet(viewsets.ModelViewSet):
    """
    List All System Yaml via Generic View
    """
    queryset = System_yaml.objects.all().order_by('name')
    serializer_class = SystemYamlSerializer


class GroupYamlViewSet(viewsets.ModelViewSet):
    """
    List All Group Yaml via Generic View
    """
    queryset = Group_yaml.objects.all().order_by('name')
    serializer_class = GroupYamlSerializer


class TenantYamlViewSet(viewsets.ModelViewSet):
    """
    List All Group Yaml via Generic View
    """
    queryset = Tenant_yaml.objects.all().order_by('name')
    serializer_class = TenantSerializer

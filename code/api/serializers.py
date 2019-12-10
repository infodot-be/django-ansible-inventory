
from .models import (Tenant, Group, System,
                     System_yaml, Group_yaml, Tenant_yaml)
from rest_framework import serializers


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='tenant-detail',
    #     lookup_field='id'
    #     )

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'yaml', 'url']
        extra_kwargs = {
            'url': {'lookup_field': 'pk'}
        }


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name', 'yaml', 'url']
        extra_kwargs = {
            'url': {'lookup_field': 'pk'}
        }


class SystemSerializer(serializers.ModelSerializer):
    # def __init__(self, *args, **kwargs):
    #     super(SystemSerializer, self).__init__(*args, **kwargs)
    #     id = serializers.UUIDField()

    class Meta:
        model = System
        fields = ['id', 'name', 'tenant', 'group', 'yaml', 'url']
        extra_kwargs = {
            'url': {'lookup_field': 'pk'}
        }


class SystemYamlSerializer(serializers.ModelSerializer):

    class Meta:
        model = System_yaml
        fields = ('id', 'name', 'url', 'text')
        lookup_field = 'id'


class GroupYamlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group_yaml
        fields = ('id', 'name', 'url', 'text')
        lookup_field = 'id'


class TenantYamlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant_yaml
        fields = ('id', 'name', 'url', 'text')
        lookup_field = 'id'

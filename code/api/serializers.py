from .models import (Customer, Group, System,
                        System_yaml, Group_yaml, Customer_yaml)
from rest_framework import serializers


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='customer-detail',
    #     lookup_field='id'
    #     )

    class Meta:
        model = Customer
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
        fields = ['id', 'name', 'customer', 'group', 'yaml', 'url']
        extra_kwargs = {
            'url': {'lookup_field': 'pk'}
        }

class SystemYamlSerializer(serializers.ModelSerializer):

    class Meta:
        model = System_yaml
        fields = ( 'id', 'name', 'url', 'text' )
        lookup_field='id'


class GroupYamlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group_yaml
        fields = ( 'id', 'name', 'url', 'text' )
        lookup_field='id'

class CustomerYamlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer_yaml
        fields = ( 'id', 'name', 'url', 'text' )
        lookup_field='id'

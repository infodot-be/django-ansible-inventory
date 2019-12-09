#!/bin/python3
"""
Ipam CLI command line interfase
"""

import os
import click
import urllib.request
from urllib.error import HTTPError
import json


class Ipam(object):
    def __init__(self, url=None, debug=False):
        self.url = url
        self.debug = debug
        if(self.debug):
            print("Debug on")

    def debug(self, debug):
        self.debug = debug

    def _post(self, django_inventory_url, new_data):
        """
        The post to the REST api
        """
        params = json.dumps(new_data).encode('utf8')
        if(self.debug):
            print("Request url : %s" % django_inventory_url)
            print("Data porvided : %s" % params)
        req = urllib.request.Request(django_inventory_url, data=params,
            headers={'content-type': 'application/json'})
        contents = urllib.request.urlopen(req).read()
        return contents.decode('utf-8')

    def _request(self, django_inventory_url):
        """
        The request form the REST api
        """
        if(self.debug):
            print("Request url : %s" % django_inventory_url)
        contents = urllib.request.urlopen(django_inventory_url).read()
        return contents.decode('utf-8')

    def tenant_exsist(self, tenant):
        """
        Check if the Tenant exsist, return the data is valid
        """
        django_inventory_url = "%s=%s" % ("http://192.168.0.5:9111/api/customer/get_by_name/?name",tenant)
        try:
            data = json.loads(self._request(django_inventory_url))
            return data[0]
        except:
            if(self.debug):
                print("Tenant not found")
            return None

    def group_exsist(self, group):
        """
        Check if a group exsist, return the data if valid
        """
        django_inventory_url = "%s=%s" % ("http://192.168.0.5:9111/api/group/get_by_name/?name",group)
        try:
            data = json.loads(self._request(django_inventory_url))
            return data[0]
        except:
            if(self.debug):
                print("Group not found")
            return None

    def list_tenants(self):
        """
        List all the tenants in the REST api.
        """
        django_inventory_url = "http://192.168.0.5:9111/api/customer/"
        try:
            data = self._request(django_inventory_url)
            json_object =json.loads(data)
            if(self.debug):
                print("Content :")
                print(json_object)
            # Output data
            for tenant in json_object:
                print(tenant['name'])
        except HTTPError as err:
            print(err.code)

    def add_tenant(self,new_data):
        """
        Add a Tenant to the REST api
        """
        django_inventory_url = "http://192.168.0.5:9111/api/customer/"
        try:
            data = self._post(django_inventory_url, new_data)
            json_object =json.loads(data)
            if(self.debug):
                print("Content :")
                print(json_object)
            # Output data if created
            print("Created : %s" % json_object['name'])
        except HTTPError as err:
            if(err.code == 400):
                print("ERROR %s : Entry exsist" % err.code)


    def list_systems(self,tenant):
        """
        List all systems for a tenant
        """
        data = self.tenant_exsist(tenant)
        if(data):
            if(self.debug):
                print("Selecting Customer: %s" % data['name'])

            django_inventory_url = "http://192.168.0.5:9111/api/system/get_by_name/?name=%s" % data['name']
            data = self._request(django_inventory_url)
            json_object = json.loads(data)
            if(self.debug):
                print("Content :")
                print(json_object)
            #Output the data
            for tenant in json_object:
                print(tenant['name'])

    def add_system(self,tenant,new_data,group):
        """
        Add a system to the REST api
        """
        tenant_data = self.tenant_exsist(tenant)
        group_data  = self.group_exsist(group)
        if(tenant_data):
            if(self.debug):
                print("Selecting Customer: %s" % tenant_data['name'])
                print("Adding to group: %s" % group_data['name'])
            django_inventory_url = "http://192.168.0.5:9111/api/system/"
            groups = list() # Groups needs to be a list
            groups.append(group_data['id'])
            new_data["customer"] = tenant_data['id']
            new_data["group"] = groups
            try:
                if(self.debug):
                    print("Trying to add %s to %s" % (new_data, tenant))
                data = self._post(django_inventory_url, new_data)
                json_object =json.loads(data)
                if(self.debug):
                    print("Content :")
                    print(json_object)
                # Output in case of added.
                print("Created : %s" % json_object['name'])
            except HTTPError as err:
                if(err.code == 400):
                    print("ERROR %s : Entry exsist" % err.code)
        else:
            print("ERROR: %s does not exsits" % tenant)


@click.group()
@click.option('--url', envvar='IPAM_API_KEY', default='blabl-url')
@click.option('--debug/--no-debug', default=False,
              envvar='REPO_DEBUG')
@click.pass_context
def cli(ctx, url, debug):
    ctx.obj = Ipam(url, debug)
    pass

@cli.command()
@click.argument('url', required=False)
def login(url):
    print(url)
    pass


@cli.command()
@click.pass_context
@click.argument('action', required=False, default=None)
@click.option('--tenant', required=True)
@click.option('--name', required=False)
@click.option('--tag', required=False)
def system(ctx, action, tag, name, tenant):
    if (action == None):
        ctx.obj.list_systems(tenant)
    elif(action == "create"):
        new_data = {"name" : name}
        ctx.obj.add_system(tenant,new_data,tag)
    else:
        print("Action %s not (yet) implemented" % action)


@cli.command()
@click.pass_context
@click.argument('action', required=False, default=None)
@click.option('--name', required=False)
def tenant(ctx, action, name):
    if (action == None):
        ctx.obj.list_tenants(action)
    elif(action == "create"):
        new_data = { "name" : name }
        ctx.obj.add_tenant(new_data)
    else:
        print("Action %s not (yet) implemented" % action)


@cli.command()
@click.argument('tag', required=False)
def tag(tag):
    print(tag)
    pass

if __name__ == "__main__":
    """
    The main application is created using the click interphase
    """
    ipam_obj = Ipam()
    cli()

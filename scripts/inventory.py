#!/bin/python3
import urllib.request
customer = "ir9_sto"
django_inventory_url = "http://192.168.0.5:9111/api/inventory/byname"
# contents = urllib.request.urlopen("http://192.168.0.5:9111/api/inventory/68401cc4-f59a-4e23-9577-ccbb15f631cd/").read()
contents = urllib.request.urlopen("%s/%s/" % (django_inventory_url, customer)).read()

print(contents.decode('utf-8'))

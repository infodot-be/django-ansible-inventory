#!/bin/python3
import urllib.request
customer = "Jedi"
django_inventory_url = "http://127.0.0.1:8000/api/inventory/byname"
contents = urllib.request.urlopen("%s/%s/" % (django_inventory_url, customer)).read()
print(contents.decode('utf-8'))

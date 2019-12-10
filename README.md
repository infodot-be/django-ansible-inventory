django-ansible-inventory
========================

[![Build Status](https://travis-ci.org/infodot-be/django-ansible-inventory.svg?branch=master)](https://travis-ci.org/infodot-be/django-ansible-inventory)

This django project will create an REST API server for dynamic inventory for Ansible.
The Ansible inventory can dynamically query this REST API during playbook execution.

The object Manipulation is done via REST API directly or the ipam-cli interface.

All objects are case sensitive in the current version.

The inventory.py script available in the scripts directory will retrieve the information and format it for Ansible

::

  []$ ansible-inventory -i inventory.py --list
  {
      "Master": {
          "hosts": [
              "obiwan.example.com",
              "yoda.example.com"
          ]
      },
      "Padawan": {
          "hosts": [
              "anakin.example.com",
              "luke.example.com"
          ]
      },
      "_meta": {
          "hostvars": {
              "anakin.example.com": {},
              "luke.example.com": {},
              "obiwan.example.com": {},
              "yoda.example.com": {}
          }
      },
      "all": {
          "children": [
              "Master",
              "Padawan",
              "ungrouped"
          ]
      }
  }

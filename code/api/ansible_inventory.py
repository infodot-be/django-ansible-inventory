from django.shortcuts import get_object_or_404
# from django.views.decorators.cache import cache_page
from .models import Tenant, Group, System, System_yaml, Group_yaml, Tenant_yaml

import yaml
import logging


class Ansible_inventory():
    def __init__(self, *args, **kwargs):
        self.tenant = kwargs['tenant']
        # self.inventory = {}
        self.group_system = {}
        self.hostvars = {}
        self.partial_inventory = {}
        self.serial_inventory = {}
        self.meta = {}
        self.ungrouped = []

        logger = logging.getLogger('Ansible_inventory')
        self.log = logger
        self.log.debug("Ansible_inventory loaded for %s" % self.tenant)
        pass

    def _process_group(self, org_group, system):
        """
        Process nested group here.
        """
        group_inventory = {}
        parent_group = get_object_or_404(Group, id=org_group.group_link.id)
        self.log.debug("org_group.name %s -> parent_group.name %s" % (org_group.name, parent_group.name))
        group_inventory[org_group.name] = {}
        try:
            self.group_system[org_group.name].append(system.name)
        except KeyError:
            self.group_system[org_group.name] = [system.name, ]

        # Retrieve and convert Group yaml
        if org_group.yaml:
            group_inventory[org_group.name]['vars'] = self._convert_yaml_to_dict(org_group.yaml.text.rstrip())

        group_inventory[org_group.name]['hosts'] = self.group_system[org_group.name]
        self.log.debug("%s" % group_inventory)
        return group_inventory

    def _convert_yaml_to_dict(self, yaml_text):
        # data = {'ansible_ssh_user': 'vagrant'}
        if (yaml_text is not None):
            data = yaml.safe_load(yaml_text.rstrip())
        else:
            data = dict()
        return data

    def _get_inventory(self, *args, **kwargs):
        """
        The request comes in from a tenant point of view.
        From that input we can get the systems beloning to the tenant.
        All groups that the system belongs to are taken into account.
        """
        # check if 'all' group exists, if no, create it
        if 'all' not in self.partial_inventory:
            self.partial_inventory['all'] = dict()
            self.partial_inventory['all']['hosts'] = list()
            self.partial_inventory['all']['vars'] = dict()
            self.partial_inventory['all']['children'] = list()
            self.partial_inventory['all']['children'].append('ungrouped')

        # Load Yaml from tenant, this can be added to the all vars sinds this will be applicable on all.
        if self.tenant.yaml:
            self.partial_inventory['all']['vars'] = self._convert_yaml_to_dict(self.tenant.yaml.text)

        # Locate all systems for the tenant
        for system in System.objects.filter(tenant=self.tenant).distinct():
            # Load Yaml from system and add this to the hostvars.
            self.hostvars[system.name] = dict()
            if system.yaml:
                self.hostvars[system.name] = self._convert_yaml_to_dict(system.yaml.text)

            ungrouped = 1
            # Loop over the groups
            for group in system.group.all():
                # The group is attached to all so add it to the childeren
                ungrouped = 0
                self.partial_inventory['all']['children'].append(group.name)
                if group.name not in self.partial_inventory:
                    self.log.debug("New group %s" % (group.name))
                    self.partial_inventory[group.name] = dict()
                    self.partial_inventory[group.name]['hosts'] = list()
                    self.partial_inventory[group.name]['vars'] = dict()
                    self.partial_inventory[group.name]['children'] = list()

                # The group has a linked item so it must be teated like this.
                # nested groups will be treated in the function.
                if group.group_link:
                    self.log.debug("Link group %s" % (group.group_link.name))

                    if group.group_link.name not in self.partial_inventory:
                        self.log.debug("New group %s" % (group.group_link.name))
                        self.partial_inventory[group.group_link.name] = dict()
                        self.partial_inventory[group.group_link.name]['hosts'] = list()
                        self.partial_inventory[group.group_link.name]['vars'] = dict()
                        self.partial_inventory[group.group_link.name]['children'] = list()
                    # Add linked gropu yaml text here
                    if group.group_link.yaml:
                        self.partial_inventory[group.group_link.name]['vars'] = self._convert_yaml_to_dict(group.group_link.yaml.text.rstrip())

                    self.log.debug("Nested Group %s adding to %s" % (group.name, group.group_link.name))
                    # self.partial_inventory[group.group_link.name] = dict()
                    self.partial_inventory[group.group_link.name]['children'] = self._process_group(group, system)
                    self.partial_inventory[group.group_link.name]['children'] = list(set(self.partial_inventory[group.group_link.name]['children']))
                    self.partial_inventory[group.group_link.name]['hosts'].append(system.name)
                    self.partial_inventory[group.group_link.name]['hosts'] = list(set(self.partial_inventory[group.group_link.name]['hosts']))  # Make unique
                else:
                    self.log.debug("Normal Group %s" % (group.name))

                self.partial_inventory[group.name]['hosts'].append(system.name)
                self.partial_inventory[group.name]['hosts'] = list(set(self.partial_inventory[group.name]['hosts']))  # Make unique
                # self.partial_inventory['all']['hosts'].append(system.name)
                # self.partial_inventory['all']['hosts'] = list(set(self.partial_inventory['all']['hosts']))  # make unique
                self.partial_inventory['all']['children'] = list(set(self.partial_inventory['all']['children']))  # make unique

            if ungrouped:
                self.ungrouped.append(system.name)

        return self.partial_inventory

    def get_inventory(self, *args, **kwargs):
        self._get_inventory(self, *args, **kwargs)
        self.partial_inventory['_meta'] = self.meta
        self.partial_inventory['_meta']['hostvars'] = self.hostvars
        self.partial_inventory['ungrouped'] = self.ungrouped
        return self.partial_inventory

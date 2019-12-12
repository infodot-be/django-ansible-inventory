from django.test import TestCase
import json
from .models import Tenant, Group, System, System_yaml, Group_yaml, Tenant_yaml

# Create your tests here.


def create_data():
    """
    Creates the test data
    """
    jedi = Tenant.objects.get(name="Jedi")
    sith = Tenant.objects.get(name="Sith")
    group_Master = Group.objects.get(name="Master")
    group_Padawan = Group.objects.get(name="Padawan")
    group_Maried = Group.objects.get(name="Maried")

    system = System.objects.create(name="mace.example.com",
                                   tenant=jedi)
    system = System.objects.create(name="maul.example.com",
                                   tenant=sith)

    system = System.objects.create(name="padme.example.com",
                                   tenant=jedi)
    system.group.add(group_Maried)
    system.yaml.text = "short_name: padme"
    system.yaml.save()

    system = System.objects.create(name="luke.example.com",
                                   tenant=jedi)
    system.group.add(group_Padawan)
    system.yaml.text = "short_name: luke\npicture: https://en.wikipedia.org/wiki/Luke_Skywalker#/media/File:Luke_Skywalker.png"
    system.yaml.save()

    system = System.objects.create(name="anakin.example.com",
                                   tenant=jedi)
    system.group.add(group_Padawan)
    system.group.add(group_Maried)
    system.yaml.text = "short_name: anakin"
    system.yaml.save()
    system = System.objects.create(name="yoda.example.com",
                                   tenant=jedi)
    system.group.add(group_Master)
    system.yaml.text = "short_name: yoda"
    system.yaml.save()
    system = System.objects.create(name="obiwan.example.com",
                                   tenant=jedi)
    system.group.add(group_Master)
    system.yaml.text = "short_name: obiwan"
    system.yaml.save()
    system = System.objects.create(name="dooku.example.com",
                                   tenant=sith)
    system.group.add(group_Master)
    system.yaml.text = "short_name: dooku"
    system.yaml.save()


class InventoryCase(TestCase):
    """ Basic testing """

    def setUp(self):
        Tenant.objects.create(name="Jedi")
        Tenant.objects.create(name="Sith")
        Group.objects.create(name="Initiate")
        Group.objects.create(name="Padawan")
        Group.objects.create(name="Knight")
        Group.objects.create(name="Master")
        Group.objects.create(name="Maried")
        create_data()

    def test_system_creation(self):
        """
        Test system creation and assigment to tenant and group
        """

        tenant = Tenant.objects.get(name="Jedi")
        systems = System.objects.filter(tenant=tenant)

        # Locating Luke in database
        found_luke = False
        for system in systems:
            if (system.name == "luke.example.com" and system.tenant.name == "Jedi"):
                found_luke = True
        self.assertTrue(found_luke, "Oh my god, Luke was not found in the database !!")

        # Locating Luke in via api
        response = self.client.get('/api/system/get_by_name/', {'name': 'luke.example.com'})
        data = json.loads(response.content.decode('utf-8'))
        record = data[0]
        self.assertEqual(record["name"], "luke.example.com", "Oh my god, Luke was not found in the api!!")

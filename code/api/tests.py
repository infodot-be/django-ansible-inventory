from django.test import TestCase
from django.urls import reverse
import json
from .models import Customer, Group, System, System_yaml, Group_yaml, Customer_yaml

# Create your tests here.


def create_data():
    """
    Creates the test data
    """
    customer = Customer.objects.get(name="Jedi")
    group_Master = Group.objects.get(name="Master")
    group_Padawan = Group.objects.get(name="Padawan")

    system = System.objects.create(name="luke.example.com",
                                   customer=customer)
    system.group.add(group_Master)
    system = System.objects.create(name="obiwan.example.com",
                                   customer=customer)
    system.group.add(group_Master)
    system = System.objects.create(name="xwingpilo.example.com",
                                   customer=customer)
    system.group.add(group_Padawan)


class InventoryCase(TestCase):
    """ Basic testing """

    def setUp(self):
        Customer.objects.create(name="Jedi")
        Customer.objects.create(name="Sith")
        Group.objects.create(name="Initiate")
        Group.objects.create(name="Padawan")
        Group.objects.create(name="Knight")
        Group.objects.create(name="Master")
        create_data()

    def test_system_creation(self):
        """
        Test system creation and assigment to customer and group
        """

        customer = Customer.objects.get(name="Jedi")
        systems = System.objects.filter(customer=customer)

        # Locating Luke in database
        found_luke = False
        for system in systems:
            if (system.name == "luke.example.com" and system.customer.name == "Jedi"):
                found_luke = True
        self.assertTrue(found_luke, "Oh my god, Luke was not found in the database !!")

        # Locating Luke in via api
        response = self.client.get('/api/system/get_by_name/', {'name': 'luke.example.com'})
        data = json.loads(response.content.decode('utf-8'))
        record = data[0]
        self.assertEqual(record["name"], "luke.example.com", "Oh my god, Luke was not found in the api!!")

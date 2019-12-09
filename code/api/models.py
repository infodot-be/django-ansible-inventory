from django.db import models
from simple_history.models import HistoricalRecords
from babel.dates import parse_date
from babel.numbers import decimal, format_decimal
import uuid

class Yaml(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    text = models.TextField(default = None, null=True, blank=True )
    # type customer,System or Group
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Yaml"

class Customer_yaml(Yaml):
    # type customer,System or Group
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Customer_yaml"

class Group_yaml(Yaml):
    # type customer,System or Group
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Group_yaml"

class System_yaml(Yaml):
    # type customer,System or Group
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "System_yaml"

class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    yaml =  models.OneToOneField(
        Customer_yaml,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customer"
        unique_together = [['name']]


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    group_link = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='group')
    yaml =  models.OneToOneField(
        Group_yaml,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Group"


class System(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    customer =  models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    group  =  models.ManyToManyField(
        Group,
        blank=True,
    )
    yaml =  models.OneToOneField(
        System_yaml,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "System"

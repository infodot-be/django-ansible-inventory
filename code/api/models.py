from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
import uuid


class Yaml(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(default=None, null=True, blank=True)
    # type Tenant,System or Group
    history = HistoricalRecords()

    def __str__(self):
        if (self.name is None):
            return str(self.id)
        else:
            return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Yaml"


class Tenant_yaml(Yaml):
    history = HistoricalRecords()

    def __str__(self):
        if (self.name is None):
            return str(self.id)
        else:
            return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Tenant_yaml"


class Group_yaml(Yaml):
    history = HistoricalRecords()

    def __str__(self):
        if (self.name is None):
            return str(self.id)
        else:
            return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "Group_yaml"


class System_yaml(Yaml):
    history = HistoricalRecords()

    def __str__(self):
        if (self.name is None):
            return str(self.id)
        else:
            return self.name

    class Meta:
        app_label = 'api'
        verbose_name_plural = "System_yaml"


class Tenant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    yaml = models.OneToOneField(
        Tenant_yaml,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Tenant"
        unique_together = [['name']]


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    group_link = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='group')
    yaml = models.OneToOneField(
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
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True)
    group = models.ManyToManyField(
        Group,
        blank=True,
    )
    yaml = models.OneToOneField(
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


"""
When a system is added the coresponding yaml_system is created
The name of the yaml by default the systemname.
"""
@receiver(post_save, sender=System)
def create_system_yaml(sender, created, instance, **kwargs):
    if created:
        if(instance.yaml is None):
            new_name = instance.name
            system_yaml = System_yaml(name=new_name)
            system_yaml.save()
            instance.yaml = system_yaml
            instance.save()

"""
When a Tenant is added the coresponding Tenant_yaml is created
The name of the yaml by default the cutomername.
"""
@receiver(post_save, sender=Tenant)
def create_tenant_yaml(sender, created, instance, **kwargs):
    if created:
        if(instance.yaml is None):
            new_name = instance.name
            tenant_yaml = Tenant_yaml(name=new_name)
            tenant_yaml.save()
            instance.yaml = tenant_yaml
            instance.save()

"""
When a Group is added the coresponding Group_yaml is created
The name of the yaml by default the Groupname.
"""
@receiver(post_save, sender=Group)
def create_group_yaml(sender, created, instance, **kwargs):
    if created:
        if(instance.yaml is None):
            new_name = instance.name
            group_yaml = Group_yaml(name=new_name)
            group_yaml.save()
            instance.yaml = group_yaml
            instance.save()

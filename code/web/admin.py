from django.contrib import admin
from api.models import Tenant, Group, System, Yaml, Tenant_yaml, Group_yaml, System_yaml
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(Tenant)
admin.site.register(Group)
admin.site.register(System)
admin.site.register(Yaml)

admin.site.register(Tenant_yaml)
admin.site.register(Group_yaml)
admin.site.register(System_yaml)

from django.contrib import admin
from api.models import Customer, Group, System, Yaml, Customer_yaml, Group_yaml, System_yaml
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.


# Register your models here.
admin.site.register(Customer)
admin.site.register(Group)
admin.site.register(System)
admin.site.register(Yaml)

admin.site.register(Customer_yaml)
admin.site.register(Group_yaml)
admin.site.register(System_yaml)

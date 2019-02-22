from django.contrib import admin
from . import models

class RoleAdmin(admin.ModelAdmin):
    pass

class User2RoleAdmin(admin.ModelAdmin):
    pass

class MenuAdmin(admin.ModelAdmin):
    pass

class PermissionAdmin(admin.ModelAdmin):
    pass

class ActionAdmin(admin.ModelAdmin):
    pass

class Permission2Action2RoleAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.User2Role, User2RoleAdmin)
admin.site.register(models.Menu, MenuAdmin)
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Action, ActionAdmin)
admin.site.register(models.Permission2Action2Role, Permission2Action2RoleAdmin)
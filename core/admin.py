from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission



class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = [field.name for field in model._meta.fields if field.name not in ['id'] ]

admin.site.register(Permission, PermissionAdmin)

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name not in ['password']]
        super(ListAdminMixin, self).__init__(model, admin_site)

from django.apps import apps
from django.db import models
from django.contrib.auth import get_user_model

model_list = apps.get_models()
#-- Monkey Patch


# for model in model_list:
#   if model != get_user_model():
#     model.add_to_class('created_by', models.CharField(max_length=250,blank=True, null=True))
#     model.add_to_class('modified_by', models.CharField(max_length=250,blank=True, null=True))

        
#   def save(self):
#       if self.pk:
#           self.created_by = request.user.id
#           self.modified_by = request.user.id
#       return super(model, self).save(*args, **kwargs)

#   model.add_to_class("save", save)


#-- Common models for all the apps
for model in model_list:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass


# CUSTOM Changes
# class UserAdmin(admin.ModelAdmin):

#   def group(self, user):
#     groups = []
#     for group in user.groups.all():
#         groups.append(group.name)
#     return ' '.join(groups)

#   group.short_description = 'Groups'
#   list_display = ('id', 'email', 'is_staff', 'group',  'first_name', 'last_name', 'date_joined')
#   list_filter = ('id', 'email')

# User = get_user_model()

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
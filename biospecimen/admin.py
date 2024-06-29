from django.contrib import admin
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,\
    Collected,ShippedWSU,ShippedECHO,User
from django.utils.translation import gettext, gettext_lazy as _
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','recruitment_location')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


UserAdmin.list_display = ('username', 'is_active', 'recruitment_location', 'is_staff')
admin.site.register(User, UserAdmin)
admin.site.register(Collection)


@admin.register(CaregiverBiospecimen)
class CaregiverBiospecimenAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('return_most_up_to_date_status',)
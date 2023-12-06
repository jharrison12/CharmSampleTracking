from django.contrib import admin
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,Processed,Stored,Outcome,Shipped,\
    CollectionType,CollectionNumber,Received,Collected,Trimester,Perinatal,ShippedWSU,ShippedECHO,User
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Collection)
admin.site.register(CollectionNumber)
admin.site.register(CollectionType)

@admin.register(CaregiverBiospecimen)
class CaregiverBiospecimenAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('return_most_up_to_date_status',)
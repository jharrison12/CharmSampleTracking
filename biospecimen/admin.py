from django.contrib import admin
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,CaregiverSurvey,Incentive,IncentiveType,SurveyOutcome,HealthcareFacility,Recruitment,ConsentVersion,\
    ConsentContract,CaregiverSocialMediaHistory,Mother,NonPrimaryCaregiver,Relation,PrimaryCaregiver, ConsentItem, ConsentType,Child,ChildName,ChildAddress,ChildAddressHistory,\
    ChildSurvey,ChildAssent,Assent,AgeCategory,Race, Ethnicity,Pregnancy, CaregiverChildRelation
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,Processed,Stored,Outcome,Shipped,\
    CollectionType,CollectionNumber,Received,Collected,Trimester,Perinatal,ShippedWSU,ShippedECHO
# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from dataview.models import User

admin.site.register(User, UserAdmin)
admin.site.register(Collection)
admin.site.register(CollectionNumber)
admin.site.register(CollectionType)

@admin.register(CaregiverBiospecimen)
class CaregiverBiospecimenAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class Status(admin.ModelAdmin):
    pass
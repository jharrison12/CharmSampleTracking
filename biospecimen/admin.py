from django.contrib import admin
from dataview.models import Caregiver,Name,CaregiverName,Address,CaregiverAddress,\
    AddressMove,Email,CaregiverEmail,Phone,CaregiverPhone, SocialMedia,CaregiverSocialMedia,CaregiverPersonalContact,\
    Project,Survey,CaregiverSurvey,Incentive,IncentiveType,SurveyOutcome,HealthcareFacility,Recruitment,ConsentVersion,\
    ConsentContract,CaregiverSocialMediaHistory,CaregiverAddressHistory,Mother,NonPrimaryCaregiver,Relation,PrimaryCaregiver, ConsentItem, ConsentType,Child,ChildName,ChildAddress,ChildAddressHistory,\
    ChildSurvey,ChildAssent,Assent,AgeCategory,Race, Ethnicity,Pregnancy, CaregiverChildRelation
from biospecimen.models import Collection,Status, CaregiverBiospecimen,ChildBiospecimen,Processed,Stored,Outcome,Shipped,\
    CollectionType,CollectionNumber,Received,Collected,Trimester,Perinatal,ShippedWSU,ShippedECHO
# Register your models here.


admin.site.register(Collection)
admin.site.register(CollectionNumber)
admin.site.register(CollectionType)

@admin.register(CaregiverBiospecimen)
class CaregiverBiospecimenAdmin(admin.ModelAdmin):
    pass
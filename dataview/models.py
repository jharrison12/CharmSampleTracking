from django.db import models

# Create your models here.
class Caregiver(models.Model):
    charm_project_identifier = models.CharField(default='', max_length=6)
    date_of_birth = models.DateField(blank=True, null=True)
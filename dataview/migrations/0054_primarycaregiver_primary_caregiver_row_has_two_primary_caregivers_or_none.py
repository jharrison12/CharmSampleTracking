# Generated by Django 4.2.3 on 2023-09-09 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0053_child_child_twin_childname'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='primarycaregiver',
            constraint=models.CheckConstraint(check=models.Q(('mother_fk__isnull', False), ('non_mother_caregiver_fk__isnull', False), _negated=True), name='primary caregiver row has two primary caregivers or none'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-11-25 13:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0003_alter_caregiveraddress_eff_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiveraddress',
            name='eff_start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 8, 16, 5, 652093)),
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caregiver',
            name='caregiver_project_identifier',
            field=models.CharField(default='', max_length=6),
        ),
    ]

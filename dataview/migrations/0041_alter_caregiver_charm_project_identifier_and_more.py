# Generated by Django 4.2.3 on 2023-08-27 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0040_alter_collection_collection_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiver',
            name='charm_project_identifier',
            field=models.CharField(default='', max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='caregiver',
            name='specimen_id',
            field=models.CharField(max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(fields=('address_line_1', 'address_line_2', 'city', 'state', 'zip_code'), name='address_not_unique'),
        ),
        migrations.AddConstraint(
            model_name='addressmove',
            constraint=models.UniqueConstraint(fields=('address_fk', 'address_move_date'), name='address_move_unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='caregiveraddress',
            constraint=models.UniqueConstraint(fields=('caregiver_fk', 'address_fk'), name='caregiver_address_constraint'),
        ),
        migrations.AddConstraint(
            model_name='caregivername',
            constraint=models.UniqueConstraint(fields=('name_fk', 'status', 'caregiver_fk'), name='name_and_status_not_unique'),
        ),
    ]
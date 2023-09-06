# Generated by Django 4.2.3 on 2023-09-02 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0042_remove_address_address_not_unique_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='incentive',
            name='incentive_unique_constraint',
        ),
        migrations.AddConstraint(
            model_name='incentive',
            constraint=models.UniqueConstraint(fields=('incentive_type_fk', 'incentive_amount'), name='incentive_unique_constraint'),
        ),
    ]
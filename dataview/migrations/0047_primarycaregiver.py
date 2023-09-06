# Generated by Django 4.2.3 on 2023-09-05 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0046_alter_caregiverbiospecimen_incentive_fk_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryCaregiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mother_fk', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='dataview.mother')),
                ('non_mother_caregiver_fk', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='dataview.nonmothercaregiver')),
            ],
        ),
    ]
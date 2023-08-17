# Generated by Django 4.2.3 on 2023-08-16 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0034_mother'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='NonMotherCaregiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caregiver_fk', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='dataview.caregiver')),
                ('relation_fk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataview.relation')),
            ],
        ),
    ]
# Generated by Django 4.2.3 on 2023-08-15 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0029_alter_recruitment_caregiver_fk'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsentVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consent_version', models.CharField(max_length=255)),
                ('consent_version_text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]

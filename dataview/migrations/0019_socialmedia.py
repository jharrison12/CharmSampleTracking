# Generated by Django 4.2.3 on 2023-08-07 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataview', '0018_rename_phone_number_fk_caregiverphone_phone_fk'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_media_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
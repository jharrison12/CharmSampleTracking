# Generated by Django 4.2.3 on 2023-09-23 00:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaregiverBiospecimen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biospecimen_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ChildBiospecimen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_date', models.DateField(default=django.utils.timezone.now)),
                ('kit_sent_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_type', models.CharField(max_length=255)),
                ('collection_number', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome', models.CharField(choices=[('C', 'Completed'), ('P', 'In Process'), ('N', 'Not Collected')], max_length=1, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Processed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collected_date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('processed_date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('logged_date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outcome_fk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='biospecimen.outcome')),
                ('processed_fk', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='biospecimen.processed')),
            ],
        ),
        migrations.AddConstraint(
            model_name='collection',
            constraint=models.UniqueConstraint(fields=('collection_type', 'collection_number'), name='collection_unique_constraint'),
        ),
        migrations.AddField(
            model_name='childbiospecimen',
            name='age_category_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataview.agecategory'),
        ),
        migrations.AddField(
            model_name='childbiospecimen',
            name='child_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataview.child'),
        ),
        migrations.AddField(
            model_name='childbiospecimen',
            name='collection_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='biospecimen.collection'),
        ),
        migrations.AddField(
            model_name='childbiospecimen',
            name='incentive_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dataview.incentive'),
        ),
        migrations.AddField(
            model_name='childbiospecimen',
            name='status_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='biospecimen.status'),
        ),
        migrations.AddField(
            model_name='caregiverbiospecimen',
            name='caregiver_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dataview.caregiver'),
        ),
        migrations.AddField(
            model_name='caregiverbiospecimen',
            name='collection_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='biospecimen.collection'),
        ),
        migrations.AddField(
            model_name='caregiverbiospecimen',
            name='incentive_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dataview.incentive'),
        ),
        migrations.AddField(
            model_name='caregiverbiospecimen',
            name='status_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='biospecimen.status'),
        ),
        migrations.AddConstraint(
            model_name='childbiospecimen',
            constraint=models.UniqueConstraint(fields=('child_fk', 'collection_fk', 'age_category_fk'), name='child biospeciment unique constraint'),
        ),
        migrations.AddConstraint(
            model_name='caregiverbiospecimen',
            constraint=models.UniqueConstraint(fields=('caregiver_fk', 'collection_fk'), name='caregiver_biospecimen_unique_constraint', violation_error_message="You can't have a duplicate item"),
        ),
    ]
# Generated by Django 3.2.3 on 2021-07-04 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_rename_postal_hawkerstall_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='hawkerstall',
            name='awards',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]

# Generated by Django 3.2.3 on 2021-07-03 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='hawkerstall',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

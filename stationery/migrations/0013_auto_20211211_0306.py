# Generated by Django 3.2.9 on 2021-12-11 03:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0012_alter_registrations_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrations',
            name='created_at',
            field=models.DateField(default=datetime.date(2021, 12, 11)),
        ),
        migrations.AddField(
            model_name='registrations',
            name='published_date',
            field=models.DateField(null=True),
        ),
    ]
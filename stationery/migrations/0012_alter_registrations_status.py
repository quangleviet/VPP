# Generated by Django 3.2.9 on 2021-12-11 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0011_alter_registrations_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrations',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Pending'), (2, 'Approved'), (3, 'Rejected')], default=0),
        ),
    ]
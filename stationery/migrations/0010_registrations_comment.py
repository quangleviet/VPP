# Generated by Django 3.2.9 on 2021-12-01 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0009_rename_regist_detail_registdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrations',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]

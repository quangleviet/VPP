# Generated by Django 3.2.8 on 2021-11-06 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0002_alter_myuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='room_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='stationery.room'),
        ),
    ]

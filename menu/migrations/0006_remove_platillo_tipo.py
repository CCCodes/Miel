# Generated by Django 2.0.5 on 2018-08-04 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20180803_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platillo',
            name='tipo',
        ),
    ]
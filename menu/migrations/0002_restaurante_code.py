# Generated by Django 2.0.5 on 2018-08-04 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurante',
            name='code',
            field=models.CharField(default=12345, max_length=100),
            preserve_default=False,
        ),
    ]

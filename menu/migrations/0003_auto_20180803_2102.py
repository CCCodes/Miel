# Generated by Django 2.0.5 on 2018-08-04 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_restaurante_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='receta',
            name='measurement',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receta',
            name='quantity',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0.5 on 2018-08-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0015_auto_20180805_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='medida',
            field=models.CharField(choices=[('oz', 'oz'), ('lb', 'lb'), ('gal', 'gal'), ('L', 'L'), ('mL', 'mL'), ('g', 'g'), ('kg', 'kg'), ('unit', 'unit'), ('dozen', 'dozen')], max_length=30),
        ),
        migrations.AlterField(
            model_name='receta',
            name='medida',
            field=models.CharField(choices=[('oz', 'oz'), ('lb', 'lb'), ('gal', 'gal'), ('L', 'L'), ('mL', 'mL'), ('g', 'g'), ('kg', 'kg'), ('unit', 'unit'), ('dozen', 'dozen')], max_length=30),
        ),
    ]

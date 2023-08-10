# Generated by Django 4.2 on 2023-08-03 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='pages',
        ),
        migrations.RemoveField(
            model_name='chart',
            name='devices',
        ),
        migrations.RemoveField(
            model_name='device',
            name='protocol',
        ),
        migrations.RemoveField(
            model_name='page',
            name='charts',
        ),
        migrations.RemoveField(
            model_name='variable',
            name='alerts',
        ),
        migrations.RemoveField(
            model_name='variable',
            name='chart_line_color',
        ),
        migrations.RemoveField(
            model_name='variable',
            name='device',
        ),
        migrations.RemoveField(
            model_name='variable',
            name='scaling',
        ),
        migrations.RemoveField(
            model_name='variable',
            name='unit',
        ),
        migrations.DeleteModel(
            name='AlertVariable',
        ),
        migrations.DeleteModel(
            name='Building',
        ),
        migrations.DeleteModel(
            name='Chart',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='Device',
        ),
        migrations.DeleteModel(
            name='DeviceProtocol',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
        migrations.DeleteModel(
            name='Scaling',
        ),
        migrations.DeleteModel(
            name='Unit',
        ),
        migrations.DeleteModel(
            name='Variable',
        ),
    ]

# Generated by Django 4.2 on 2023-08-09 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebService',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Web service name')),
                ('method', models.CharField(choices=[(0, 'Path'), (1, 'GET')], max_length=10, verbose_name='Method to get data')),
                ('contentType', models.CharField(choices=[(0, 'JSON'), (1, 'XML')], max_length=30, verbose_name='Content of device response')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
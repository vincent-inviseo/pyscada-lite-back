# Generated by Django 4.2 on 2023-08-10 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0004_chart_charttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceprotocol',
            name='protocol',
            field=models.IntegerField(choices=[(0, 'Web Service'), (1, 'Modbus'), (2, 'BacNet')], max_length=2),
        ),
    ]
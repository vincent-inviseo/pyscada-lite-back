# Generated by Django 4.2 on 2023-08-28 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0025_alter_chart_charttype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variablevalues',
            name='value',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

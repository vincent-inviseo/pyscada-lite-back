# Generated by Django 4.2 on 2023-08-11 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0011_variablevalues_remove_variable_value_variable_values'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variable',
            name='device',
        ),
        migrations.AddField(
            model_name='device',
            name='variables',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.variable'),
        ),
    ]

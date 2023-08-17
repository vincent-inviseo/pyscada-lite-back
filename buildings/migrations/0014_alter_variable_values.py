# Generated by Django 4.2 on 2023-08-11 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0013_alter_device_variables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variable',
            name='values',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.variablevalues'),
        ),
    ]
# Generated by Django 4.2.3 on 2023-08-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0018_variable_webservice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='widht',
            new_name='width',
        ),
        migrations.AlterField(
            model_name='chart',
            name='updatedAt',
            field=models.DateTimeField(blank=True),
        ),
    ]
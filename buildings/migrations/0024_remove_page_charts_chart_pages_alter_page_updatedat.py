# Generated by Django 4.2.3 on 2023-08-17 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0023_alter_building_updatedat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='charts',
        ),
        migrations.AddField(
            model_name='chart',
            name='pages',
            field=models.ManyToManyField(to='buildings.page'),
        ),
        migrations.AlterField(
            model_name='page',
            name='updatedAt',
            field=models.DateTimeField(),
        ),
    ]

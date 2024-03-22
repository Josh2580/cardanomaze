# Generated by Django 5.0.3 on 2024-03-20 07:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0004_rename_first_clicked_mining_first_click'),
    ]

    operations = [
        migrations.AddField(
            model_name='mining',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='mining',
            name='remaining_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

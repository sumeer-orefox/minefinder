# Generated by Django 4.2 on 2023-04-19 00:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_public_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='public_fields',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(default=False), blank=True, default=list, size=None),
        ),
    ]

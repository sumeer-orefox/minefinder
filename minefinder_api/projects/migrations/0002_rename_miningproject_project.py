# Generated by Django 4.2 on 2023-04-13 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MiningProject',
            new_name='Project',
        ),
    ]
# Generated by Django 4.2 on 2023-04-19 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_userprofile_contact_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='contact_no',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]

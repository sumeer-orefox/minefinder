# Generated by Django 4.2 on 2023-04-17 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ('date_joined',)},
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='about',
            new_name='bio',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='created_at',
            new_name='date_joined',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='updated_at',
            new_name='date_updated',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='company',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-13 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_researchedcities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_permissions',
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-24 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_date_receita_researchedcities_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchedcities',
            name='country',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]

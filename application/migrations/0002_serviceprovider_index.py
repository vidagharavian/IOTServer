# Generated by Django 4.2.7 on 2023-11-07 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
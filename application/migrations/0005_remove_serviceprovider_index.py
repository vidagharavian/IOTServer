# Generated by Django 4.2.7 on 2023-11-15 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_alter_spframe_creation_date_alter_spframe_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceprovider',
            name='index',
        ),
    ]

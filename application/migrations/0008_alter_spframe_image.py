# Generated by Django 4.2.7 on 2023-11-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_alter_spframe_head_coordinate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spframe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='templates/image/'),
        ),
    ]
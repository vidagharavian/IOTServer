# Generated by Django 4.2.7 on 2023-11-20 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_alter_spframe_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.service')),
                ('service_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.serviceprovider')),
            ],
        ),
    ]
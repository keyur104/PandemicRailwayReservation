# Generated by Django 2.2.1 on 2020-07-01 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Railway', '0014_registration_medical'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='medical',
        ),
    ]
# Generated by Django 2.2.5 on 2020-07-11 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Railway', '0021_auto_20200701_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mahanagari_express_seat_alloc',
            old_name='Date',
            new_name='date',
        ),
    ]

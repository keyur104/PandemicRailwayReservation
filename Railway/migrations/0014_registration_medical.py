# Generated by Django 2.2.1 on 2020-07-01 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Railway', '0013_auto_20200629_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='medical',
            field=models.ImageField(default='NULL', upload_to=''),
            preserve_default=False,
        ),
    ]
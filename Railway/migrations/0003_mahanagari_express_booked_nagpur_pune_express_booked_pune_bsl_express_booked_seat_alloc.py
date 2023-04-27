# Generated by Django 2.2.1 on 2020-06-25 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Railway', '0002_mahanagari_express_seat_alloc_nagpur_pune_express_seat_alloc_pune_bsl_express_seat_alloc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mahanagari_Express_Booked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
                ('seat', models.CharField(max_length=10)),
                ('source', models.CharField(max_length=30)),
                ('destination', models.CharField(max_length=30)),
                ('date_of_journey', models.DateField()),
                ('name', models.CharField(max_length=40)),
                ('birth_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Nagpur_Pune_Express_Booked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
                ('seat', models.CharField(max_length=10)),
                ('source', models.CharField(max_length=30)),
                ('destination', models.CharField(max_length=30)),
                ('date_of_journey', models.DateField()),
                ('name', models.CharField(max_length=40)),
                ('birth_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Pune_Bsl_Express_Booked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
                ('seat', models.CharField(max_length=10)),
                ('source', models.CharField(max_length=30)),
                ('destination', models.CharField(max_length=30)),
                ('date_of_journey', models.DateField()),
                ('name', models.CharField(max_length=40)),
                ('birth_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Seat_Alloc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_no', models.CharField(max_length=10)),
                ('class_type', models.CharField(max_length=10)),
                ('birth_type', models.CharField(max_length=10)),
            ],
        ),
    ]

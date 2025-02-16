# Generated by Django 3.2.19 on 2025-02-13 18:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateField()),
                ('pickup_date', models.DateField()),
                ('return_date', models.DateField()),
                ('pickup_time', models.TimeField(default=datetime.time(9, 0))),
                ('drop_time', models.TimeField(default=datetime.time(17, 0))),
                ('destination', models.CharField(max_length=255)),
                ('total_price', models.FloatField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('canceled', 'Canceled')], default='active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('fuel', models.CharField(max_length=50)),
                ('seats', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('amount', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='cars/')),
            ],
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='cars.car')),
                ('pickup_date', models.DateField()),
                ('return_date', models.DateField()),
                ('available_quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cancellation',
            fields=[
                ('cancellation_id', models.AutoField(primary_key=True, serialize=False)),
                ('cancellation_date', models.DateField()),
                ('reason', models.TextField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.car'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-23 22:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=5)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=5, unique=True, validators=[django.core.validators.RegexValidator('\\d{4}[A-Z]{1}')])),
                ('load_capacity', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10000)])),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.location')),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10000)])),
                ('description', models.CharField(max_length=1000)),
                ('delivery_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargo_delivery', to='api.location')),
                ('pickup_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargo_pickup', to='api.location')),
            ],
        ),
    ]
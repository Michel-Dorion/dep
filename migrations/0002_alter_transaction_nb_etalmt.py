# Generated by Django 3.2.3 on 2022-01-04 16:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='nb_etalmt',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(11)]),
        ),
    ]
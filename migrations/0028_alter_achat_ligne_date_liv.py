# Generated by Django 3.2.5 on 2022-02-11 16:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0027_transaction_date_tx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achat_ligne',
            name='date_liv',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]

# Generated by Django 3.2.5 on 2022-01-29 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0007_remove_transaction_moyen_paiemt_utilise'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='intitule',
            field=models.CharField(blank=True, default='', max_length=12),
        ),
    ]

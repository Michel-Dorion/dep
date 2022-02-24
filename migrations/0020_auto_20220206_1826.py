# Generated by Django 3.2.5 on 2022-02-06 18:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0019_auto_20220205_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fournisseur_regulier',
            name='articles_hab',
        ),
        migrations.RemoveField(
            model_name='fournisseur_regulier',
            name='objet_tx_hab',
        ),
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='nature_achat_hab',
            field=models.CharField(choices=[('F', 'Consommable'), ('S', 'Service'), ('D', 'Bien Durable'), ('A', 'Autre')], default='', max_length=1),
        ),
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='nature_tx_hab',
            field=models.CharField(blank=True, choices=[('UNIT', 'Unitaire'), ('LIV', 'A Livraison'), ('ABMT', 'Abonnement')], default='F', max_length=4),
        ),
        migrations.AlterField(
            model_name='mouvmt_engage',
            name='jour_ds_periode',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(28)]),
        ),
    ]
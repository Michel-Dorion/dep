# Generated by Django 3.2.5 on 2022-02-05 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0018_auto_20220205_1321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fournisseur_regulier',
            old_name='intitule',
            new_name='intitule_tx_hab',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='intitule',
            new_name='intitule_tx',
        ),
        migrations.AddField(
            model_name='achat_ligne',
            name='nature_achat',
            field=models.CharField(choices=[('F', 'Consommable'), ('S', 'Service'), ('B', 'Bien Durable'), ('D', 'Don'), ('A', 'Autre')], default='F', max_length=1),
        ),
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='nom_fourn',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
    ]

# Generated by Django 3.2.5 on 2022-02-07 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0021_remove_transaction_objet_tx'),
    ]

    operations = [
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='compte_bancaire_hab',
            field=models.CharField(choices=[('F', 'Fortuneo'), ('C', 'CIC'), ('E', 'Liquide en €')], default='F', max_length=3),
        ),
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='intitule_hab',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='moyen_paiemt_hab',
            field=models.CharField(choices=[('CB_A', 'CB Annie'), ('CB_M', 'CB Michel'), ('CVU_M', 'CV_A usage unique'), ('CVU_M', 'CV_M usage unique'), ('CVA_M', 'CV_A pls debits'), ('CVA_M', 'CV_M pls debits'), ('DAB', 'Retrait'), ('ESP', 'Espèce'), ('CHQ', 'Cheque'), ('VRMT', 'Virement'), ('PbP', 'Pay by Phone'), ('CASM', 'CasinoMax')], default='CB_M', max_length=5),
        ),
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='nature_paiemt_hab',
            field=models.CharField(choices=[('ORD', 'Integral'), ('ACC', 'Accompte'), ('ETA', 'Etalement'), ('SOL', 'Solde'), ('ARH', 'Arrhes')], default='ORD', max_length=3),
        ),
        migrations.AddField(
            model_name='fournisseur_regulier',
            name='solo_tx',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='achat_ligne',
            name='montant',
            field=models.DecimalField(decimal_places=2, default='', max_digits=8),
        ),
    ]

# Generated by Django 3.2.5 on 2022-01-24 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0002_alter_transaction_nb_etalmt'),
    ]

    operations = [
        migrations.AddField(
            model_name='achat_ligne',
            name='categorie_autre',
            field=models.CharField(blank=True, choices=[('ALIM', 'Alimentation'), ('ENTRET', 'Entretien'), ('SANTE', 'Sante'), ('ENERG', 'Energie'), ('VEMTS', 'Vetements'), ('DEPCMT', 'Deplacement'), ('A_FNMT', 'Autre')], default='', max_length=16),
        ),
        migrations.AddField(
            model_name='achat_ligne',
            name='categorie_fnmt',
            field=models.CharField(blank=True, choices=[('ALIM', 'Alimentation'), ('ENTRET', 'Entretien'), ('SANTE', 'Sante'), ('ENERG', 'Energie'), ('VEMTS', 'Vetements'), ('DEPCMT', 'Deplacement'), ('A_FNMT', 'Autre')], default='', max_length=16),
        ),
        migrations.AddField(
            model_name='achat_ligne',
            name='categorie_gest',
            field=models.CharField(blank=True, choices=[('ALIM', 'Alimentation'), ('ENTRET', 'Entretien'), ('SANTE', 'Sante'), ('ENERG', 'Energie'), ('VEMTS', 'Vetements'), ('DEPCMT', 'Deplacement'), ('A_FNMT', 'Autre')], default='', max_length=16),
        ),
        migrations.AddField(
            model_name='achat_ligne',
            name='categorie_loisir',
            field=models.CharField(blank=True, choices=[('ALIM', 'Alimentation'), ('ENTRET', 'Entretien'), ('SANTE', 'Sante'), ('ENERG', 'Energie'), ('VEMTS', 'Vetements'), ('DEPCMT', 'Deplacement'), ('A_FNMT', 'Autre')], default='', max_length=16),
        ),
        migrations.AddField(
            model_name='achat_ligne',
            name='categorie_prod',
            field=models.CharField(blank=True, choices=[('ALIM', 'Alimentation'), ('ENTRET', 'Entretien'), ('SANTE', 'Sante'), ('ENERG', 'Energie'), ('VEMTS', 'Vetements'), ('DEPCMT', 'Deplacement'), ('A_FNMT', 'Autre')], default='', max_length=16),
        ),
        migrations.AddField(
            model_name='mouvmt_engage',
            name='renouv_auto',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='achat_ligne',
            name='nature_achat',
            field=models.CharField(choices=[('F', 'Consommable'), ('S', 'Service'), ('D', 'Bien Durable'), ('A', 'Autre')], default='F', max_length=1),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='fournisseur',
            field=models.CharField(max_length=18),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='mode_reglmnt',
            field=models.CharField(choices=[('CPT', 'au Comptant'), ('ETA', 'en Plusieurs fois'), ('CRE', 'a Credit')], default='CPT', max_length=3),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='nature_tx',
            field=models.CharField(choices=[('UNIT', 'Unitaire'), ('ABMT', 'Abonnement')], default='UNIT', max_length=4),
        ),
    ]

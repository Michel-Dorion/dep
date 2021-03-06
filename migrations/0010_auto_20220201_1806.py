# Generated by Django 3.2.5 on 2022-02-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep', '0009_alter_transaction_intitule'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='solo_tx',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mouvmt_fin',
            name='compte_bancaire',
            field=models.CharField(choices=[('F', 'Fortuneo'), ('C', 'CIC'), ('E', 'Liquide en €')], default='F', max_length=3),
        ),
    ]

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.urls import reverse
from datetime import date, timedelta
#from django.utils import timezone



# Create your models here.


class SelectionTx(): #accompagne la saisie d'une transaction
#nature_transaction
    UNITAIRE = 'UNIT'
    LIVRAISON = 'LIV'
    ABNMT = 'ABMT'
    REMBSMT ='RBSM'
    def chx_nature_tx(self):
        return [(self.UNITAIRE, 'Unitaire'), (self.LIVRAISON, 'A Livraison'), (self.ABNMT, 'Abonnement'), (self.REMBSMT, 'Remboursement')]
#mode_reglement
    COMPTANT = 'CPT'
    ETALE = 'ETA'
    CREDIT = 'CRE'
    def chx_mode_reglmt(self):
        return [(self.COMPTANT, 'Comptant'), (self.ETALE, 'Etalmt'), (self.CREDIT, 'Credit') ]


class SelectionPaiemt(): #accompagne les mouvmts
# nature paiemt
    ACCOMPTE ='ACC' #engage les 2 parties
    ARRHES = 'ARH' # les 2 parties peuvent revenir sur leur decision
    ETALMT = 'ETA'
    SOLDE = 'SOL'
    ORDIN = 'ORD'
    def chx_nature_paiemt(self):
        return [(self.ORDIN, 'Integral'), (self.ACCOMPTE, 'Accompte'), (self.ETALMT, 'Etalement'), (self.SOLDE, 'Solde'), (self.ARRHES, 'Arrhes')]
#compte bancaire
    FORT = 'F'
    CIC ='C'
    LIQUIDE_EURO ='E'
    def chx_compte_bancaire(self):
        return [(self.FORT, 'Fortuneo'), (self.CIC,'CIC'), (self.LIQUIDE_EURO, 'Liquide en €')]
#moyen paiement
    CB_Annie = 'CB_A'
    CB_Michel = 'CB_M'
    CV_CT_Annie = 'CVU_A'  # valid 1mois sur CB Annie
    CV_CT_Michel = 'CVU_M'  # valid 1mois sur CB Michel
    CV_LT_Annie = 'CVD_M'    # valid jusqa 12mois pour abnmt sur CB Annie
    CV_LT_Michel = 'CVD_M'    # valid jusqa 12mois pour abnmt sur CB Michel
    RETRAIT = 'DAB'         # pas carte de retrait DAB sur CIC
    ESPECE = 'ESP'
    CHEQUE = 'CHQ'   #emis ou recu
    VIREMENT ='VRMT'  #emis ou reçu
    SEPA = 'SEPA'
    PAY_BY_PHONE = 'PbP'
    CASINO_MAX = 'CASM'
    AVOIR = 'AVOIR'

    def chx_moyen_paiemt(self):
        return [(self.CB_Annie, 'CB Annie'), (self.CB_Michel, 'CB Michel'),
        (self.CV_CT_Annie, 'CV_A usage unique'), (self.CV_CT_Michel, 'CV_M usage unique'),
        (self.CV_LT_Annie, 'CV_A pls debits'), (self.CV_LT_Michel, 'CV_M pls debits'),
        (self.RETRAIT, 'Retrait'), (self.ESPECE, 'Espèce'), (self.CHEQUE, 'Cheque'), (self.VIREMENT, 'Virement'),
        (self.SEPA, 'Prélèvmt Automatiq'), (self.PAY_BY_PHONE, 'Pay by Phone'), (self.CASINO_MAX, 'CasinoMax'), (self.AVOIR, 'Avoir')]

class SelectionCategorieAchat(): #accompagne les lignes d'achat
# nature d'achat
    FOURNITURE = 'F'
    SERVICE = 'S'
    DURABLE = 'D'
    def chx_nature_achat(self):
        return [(self.FOURNITURE, 'Consommable'), (self.SERVICE, 'Service'), (self.DURABLE, 'Bien Durable')]
# groupes d'achat
    FNMT ='FNMT'
    GEST ='GEST'
    LOISIR ='LOIS'
    PROD ='PROD'
    AUTRE ='AUTR'
    def chx_groupe_achat(self):
        return [(self.FNMT, 'FNMT'), (self.GEST,'GESTION'), (self.LOISIR,'LOISIR'), (self.PROD,'PROD'), (self.AUTRE, 'Autre groupe')]
# groupe FNMT
    ALIM = 'ALIM'
    ENTRETIEN ='ENTRET'
    TOILETTE = 'TOILET'
    SANTE = 'SANTE'
    ENERGIE = 'ENERG'  #énergie domicile
    VETMTS = 'VEMTS'
    DEPLCMT = 'DEPCMT'  #carburant en consommable lavage et entretien en service
    def chx_cat_fnmt(self):
        return [(self.ALIM, 'Alimentation'), (self.ENTRETIEN, 'Entretien'), (self.TOILETTE, 'Toilette'), (self.SANTE, 'Sante'), \
                        (self.ENERGIE, 'Energie'), (self.VETMTS, 'Vetements'), (self.DEPLCMT, 'Deplacement')]
#DS LE GROUPE GEST
    SUIVIS ='INFOS'
    LOGMT = 'LOGMT'
    INFQ = 'INFQ'
    COMM = 'COMM'
    FIN = 'BQE'
    ASS = 'ASSUR'
    def chx_cat_gest(self):
        return [(self.SUIVIS, 'Infos'), (self.LOGMT, 'Logement'), (self.INFQ, 'Informatique'), (self.COMM, 'Communications'), \
                        (self.FIN, 'Finances'), (self.ASS, 'Assurances')]
#DS LE GROUPE LOISIR
    SPORT = 'SPRT'
    CULT = 'CULT'
    VACANCES = 'VACNC'
    def chx_cat_loisir(self):
        return [(self.SPORT, 'Sport'), (self.CULT, 'Culture'), (self.VACANCES, 'Vacances')]
#DS LE GROUPE PROD
    PATRIM = 'GEST PATRIM'
    SVF = 'SVF'
    TRVX = 'TRVX'
    DECO ='DECO'
    COUTUR = 'COUTUR'
    AUTRE_PROD = 'A_PROD'
    def chx_cat_prod(self):
        return [(self.PATRIM, 'Patrimoine'), (self.SVF, 'Savoir Faire'), (self.TRVX, 'Travaux/Répar'),
                (self.DECO, 'Decoration'), (self.COUTUR, 'Couture/Tricot')]

    def chx_categorie_achat(self):
        return [(self.FNMT, self.chx_cat_fnmt()), (self.GEST, self.chx_cat_gest()),
                (self.LOISIR, self.chx_cat_loisir()), (self.PROD, self.chx_cat_prod()), ('AUTR', 'Autre ds le groupe') ] #,(self.AUTRE,'AUTRE')


class Fournisseur_regulier(models.Model):
    # avoir tjrs le meme intitule pour les fournisseur régiliers

    s_t = SelectionTx()
    s_p = SelectionPaiemt()
    c_a = SelectionCategorieAchat()
    #print("selection cat d'achat", c_a.chx_categorie_achat())

    #print('chx nature paiemt', s_p.chx_nature_paiemt())

    nom_fourn = models.CharField(max_length=32, blank=True, default='') # nom du fournisseur regulier
    adresse_rue = models.CharField(max_length=24, blank=True, default='')
    adresse_ville = models.CharField(max_length=24, blank=True, default='')
    adresse_mel = models.EmailField(max_length=24, blank=True, default='')
    tel_magasin = models.CharField(max_length=10, blank=True, default='')
    tel_contact = models.CharField(max_length=10, blank=True, default='')
    #pour les tx habituelles répétitives saise auto des champs
    intitule_tx_hab = models.CharField(max_length=32, blank=True, default='')
    solo_tx_hab = models.BooleanField(default=False) # une seule categorie pour creation auto ligne d'achat associee pour une tx d1 fourn rég
    nature_tx_hab = models.CharField(max_length=4, choices=s_t.chx_nature_tx(), blank=True, default='F') # en fait nature_tx_hab
    #pour la saisie automatiq d'un mouvmt
    nature_paiemt_hab = models.CharField(max_length=3, choices=s_p.chx_nature_paiemt() , default='ORD')
    compte_bancaire_hab = models.CharField(max_length=3, choices=s_p.chx_compte_bancaire(), default='F')
    moyen_paiemt_hab = models.CharField(max_length=5, choices=s_p.chx_moyen_paiemt(), default='CB_M') #pour tx UNIT

    # saisie automatiq  d'une ligne achat pour les tx mono categorie ou base pour multi catégorie
    intitule_hab = models.CharField(max_length=32, blank=True, default='')  # sert de base pour sold achat type carrefour
    nature_achat_hab = models.CharField(max_length=1, choices=c_a.chx_nature_achat(), default='')
    groupe_achat_hab = models.CharField(max_length=16, blank=True, choices=c_a.chx_groupe_achat(), default='' ) # FNMT, LOISIR, ...
    categorie_achat_hab = models.CharField(max_length=16, choices=c_a.chx_categorie_achat(), blank=True, default='' ) #dans le groupe



    def __str__(self):
        return self.nom_fourn + ' ' + self.adresse_ville

class MdcUtils:
    @classmethod
    def laVeille(self):
        return date.today() - timedelta(days=1)

class Transaction(models.Model):
    #création à la commande

    s_t = SelectionTx()

    #champs
    #fournisseur_reg = models.ForeignKey(Fournisseur_regulier, null=True) # faut pouvoir supprimer un fourn reg sans supp ses tx
    fournisseur = models.CharField(max_length=32, blank=True, default='')
    date_tx = models.DateField(default=MdcUtils.laVeille, blank=True) #date de l'opération par default, celle de la saisie
    intitule_tx = models.CharField(max_length=32, blank=True, default='')
    nature_tx = models.CharField(max_length=4, choices=s_t.chx_nature_tx(), default='UNIT')
    renouv_auto_tx = models.BooleanField(default=False)
    date_tx_enrgt = models.DateField(auto_now_add=True) #date d'enrgmt, pas date de l'opération
    montant_tx = models.DecimalField(max_digits=8,decimal_places=2)
    #objet_tx = models.CharField(max_length=1, choices=chx_objet_tx, default=FOURNITURE) # catégorisation pas ici
    solo_tx = models.BooleanField(default=False) # une seule categorie pour creation auto ligne d'achat associee pour une tx d1 fourn rég
    mode_reglmnt = models.CharField(max_length=3, choices=s_t.chx_mode_reglmt(), default='CPT')
    nb_etalmt = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(11)])
    versmt_initial = models.DecimalField(max_digits=8,decimal_places=2, default=0)

    def get_absolute_url(self):
        return '/dep/'  # reverse('dep_url') 'dep_url' is not a valid view function or pattern name.

    def __str__(self):
        return self.date_tx.strftime("%d-%m-%Y") + ' ' + self.fournisseur + ' : ' + self.intitule_tx


class Mouvmt_fin(models.Model):
    # le paiement d une transaction
    s_p = SelectionPaiemt()

    #champs
    tx_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)   # changer le nom en tx car c l'instance Transaction qui est traitee
    nature_paiemt = models.CharField(max_length=3, choices=s_p.chx_nature_paiemt(), default='ORD')
    compte_bancaire = models.CharField(max_length=3, choices=s_p.chx_compte_bancaire(), default='F')
    moyen_paiemt = models.CharField(max_length=5, choices=s_p.chx_moyen_paiemt(), default='CB_M') #pour tx UNIT
    fin_validite_mp = models.DateField(default=date.today)



class Mouvmt_courant(Mouvmt_fin):


    # revoir cette sous classe car il y aura 2 tables crees  avec pointage vers la table parent avec creation d1 index arriere
    date_mvmt = models.DateField(default=MdcUtils.laVeille, blank=True)
    #date_mvmt_old = models.DateField(default=date.today, blank=True)
    montant_mvmt = models.DecimalField(max_digits=8,decimal_places=2) #, default=tx_id.get_montant_tx_display())
    rapprochmt_bqe = models.BooleanField(default=False)

    def get_absolute_url(self):
        return '/dep/'  # reverse('dep_url') 'dep_url' is not a valid view function or pattern name.

    def __str__(self):
        return self.date_mvmt.strftime("%d-%m-%Y") + ' | ' + str(self.montant_mvmt) + ' € , '
        #return  str(self.montant_mvmt) + ' € , '


class Mouvmt_engage(Mouvmt_fin):
    #periode
    PART = 'P' # etalement sur qq mois mois
    LIV = 'L'  # solde a la livraison
    # recurrentes
    MOIS = 'M'
    TRIM = 'T'
    SEMEST = 'S'
    AN = 'A'
    chx_periode = [(PART, 'en pls fois'), (LIV, 'solde a livraison'), (MOIS, 'Mois'), (TRIM, 'Trimestre'), (SEMEST, 'Semestre'), (AN, 'Annuel')]

    periode = models.CharField(max_length=1, choices=chx_periode, default=MOIS)
    jour_ds_periode = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(28)]) # 28 pour dernier j du mois
    mois_ds_periode = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(12)]) #pour periode > mois
    #nb_etalmt = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(12)]) # pour abnmt avec regul tye edf
    montant_precedent = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    montant_annonce = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    effectif_ds_n_periode = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(12)]) # en general pour l'echeance suivante
    renouv_auto = models.BooleanField(default=False)
    horodate_dern_conv = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return '/dep/'  # reverse('dep_url') 'dep_url' is not a valid view function or pattern name.

    def __str__(self):
        return  self.periode + ' le ' + str(self.jour_ds_periode) + '/' + str(self.mois_ds_periode) + ': ' + str(self.montant_annonce) + ' € '


class Achat_ligne(models.Model):
    # les tx de type virmt interne ou retrait DAB ne donne pas lieu à ligne achat : ni tx solo ni création manuelle

    s_a = SelectionCategorieAchat()


    tx_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    intitule = models.CharField(max_length=32)
    montant = models.DecimalField(max_digits=8,decimal_places=2, default='')
    date_liv = models.DateField(default=date.today, blank=True)
    nature_achat = models.CharField(max_length=1, choices=s_a.chx_nature_achat(), default='F')
    groupe_achat = models.CharField(max_length=4, choices=s_a.chx_groupe_achat(), default='FNMT')
    categorie_achat = models.CharField(max_length=16, choices=s_a.chx_categorie_achat(), blank=True, default='' )


    def __str__(self) :
        return self.intitule + ' le ' + self.date_liv.strftime("%d-%m-%Y")
"""


    # ss categorie dépense TROP FIN

    BOULANGE = 'BOU'
    FRUIT_LEGUME ='FLE'
    LAIIER = 'LAI'
    BOISSON = 'BOI'
    CONSERVE = 'CON'
    VIANDE_POISSON = 'VIA'
    chx_type_alim = [(BOULANGE, 'AL:Boulangerie Patisserie'), (FRUIT_LEGUME, 'AL:Fruits Légumes'), (BOISSON, 'AL:Boisson'),
                    (CONSERVE, 'AL:Conserve'), (LAIIER, 'AL:Produits Laitiers'),(VIANDE_POISSON, 'AL:Viande Poisson')]
    #ds FNMT
    MENAGER = 'MEN'
    CORPOREL = 'COR'
    VAISSELLE_CUISINE = 'VCU'
    LINGE_MAISON = 'LMA'
    FOURN_PLANTE = 'FPL'
    FOURN_BRICO = 'FBR'
    FOURN_BUREAU = 'FBU'
    FOURN_COUTURE = 'FCO'
    FOURN_ELEC = 'FEL'
    BEAUTE = 'BEA'
    chx_type_fnmt = [(MENAGER, 'FO:Produits Menagers'), (CORPOREL, 'FO:Produits Hygiène du Corps'), (VAISSELLE_CUISINE, 'FO:Vaisselle Cuisine'),
                    (LINGE_MAISON, 'FO:Linge Maison'), (FOURN_PLANTE, 'FO:Fournitures Plantes'), (FOURN_BRICO, 'FO:Fournitures Bricolage'),
                    (FOURN_BUREAU, 'FO:Fournitures Bureau'), (FOURN_COUTURE, 'FO:Fournitures Couture'),
                    (FOURN_ELEC, 'FO:Fournitures Electriques'), (BEAUTE, 'FO:Produits de Beaute') ]
    # ds LOGMT
    ASSUR_MRH = 'MRH'
    CHARGES = 'CHA'
    TAXE_FONCIERE = 'TFO'
    ELECTICITE = 'ELE'
    TAXE_HABITAT = 'THA'
    TRVX_APPART = 'TAP'
    INFOS = 'INF'
    #ds SVCES
    TELECOMM = 'TEL'
    POSTAL = 'POS'
    JURIDIQ_ADMIN = 'JAD'
    BANQUE_FIN = 'BFI'
    COURS_SVF = 'COU'
    SVC_SPO = 'SSP'
    RESTAU_HOTEL = 'RHO'
    #ds SANTE
    PHARMA = 'PHA'
    CONSULT = 'CNS'
    RADIOLO = 'RAD'
    LABO = 'LAB'
    CHIRURG = 'CHI'
    PROTHESE = 'PRO'
    SOIN = 'SOI'
    #ds CULTURE
    REVUE = 'REV'
    OEUVRE_VIDEO = 'OVI'
    OEUVRE_AUDIO = 'OAU'
    LIVRE ='LIV'
    BILLET_EVT ='BEV'
    CADEAUX = 'CAD'
    RECEPTION = 'REC'
    #ds EQPMTS
    SPORTIF = 'SPO'
    VETEMENT = 'VET'
    LOGICIELS = 'LOG'
    MOBILIER = 'MOB'
    VAISSELLE_RECEPTION = 'VRE'
    ELECTROMENAGER = 'EME'
    PLANTES = 'PLA'
    OUTILS = 'OUT'
    CAMPING = 'CAM'
    DECO = 'DEC'
    APPAREIL_AVC = 'AVC'
    #ds TRSPRT
    PARKING = 'PAR'
    CARBURANT = 'CAR'
    PEAGE = 'PEA'
    ENTRETIEN = 'ENT'
    ASSUR_VEHICULE = 'AVE'
    TRSPRT_COMMUN = 'TCO'

    categorie = models.CharField(max_length=2, choices=chx_categorie, default=ALIM)
    type = models.CharField(max_length=3, choices= chx_type_alim+chx_type_fnmt)





class Bien_durable(models.Model):
    # creation a la livraison
    fonction = models.CharField(max_length=12)
    marque = models.CharField(blank=True, max_length=12)
    modele = models.CharField(blank=True, max_length=12)
    duree_garantie = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)]) #en année
    date_liv = models.DateField(auto_now_add=True)
    ligne_achat_id = models.ForeignKey(Achat_ligne, on_delete=models.CASCADE)
    prix_ttc = models.DecimalField(max_digits=8,decimal_places=2)
    numero_facture =  models.CharField(blank=True, max_length=10)


class Activité(models.Model):

    ligne_achat_id = models.ForeignKey(Achat_ligne, on_delete=models.CASCADE)
    activités = [ 'Fnmt_Person', 'Fnmt_Dom', 'Maintien_Dom', 'Maintien_Person', 'Gest_Fin', 'Loisirs', 'Svf']

    pour_fnmt_person = [ 'Alim', 'Prdts_Corps' ]
    pour_fnmt_dom = ['Prdt_Menager', 'Vaisselle_Cuisine', 'Energie_dom', 'Charge_dom', 'Eqpmnt_dom', 'Comm_dom']
    maintien_dom = ['Reparations', 'Amel_fnl', 'Amel_deco']
    maintien_person = ['Sante', 'Gym', 'Vetement_dom', 'Vetement_ville']
    deplacmt = ['Eqpmt_transprt', 'Svce_transport', 'Eqpmts_herbergmt', 'Svces_herbergement']
    gest_fin = ['Suivi_envmt_fin', 'Eqpmts_gest', 'Svces_fin']
    loisirs = ['Suivi_loisir', 'Eqpmts_sport', 'Svces_sport', 'Eqpmts_cult', 'Svces_cult']
    svf =  ['Maintien_svf', 'Eqpmts_svf']
    # eqpmts multi activités range ds l'activite principale ordimm loisir, ordisvf

"""





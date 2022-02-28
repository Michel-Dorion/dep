
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
    ENERGIE = 'E'
    SERVICE = 'S'
    OEUVRE = 'O'
    DURABLE = 'D'
    def chx_nature_achat(self):
        return [(self.FOURNITURE, 'Consommable'), (self.SERVICE, 'Service'), (self.OEUVRE, 'Oeuvre'), 
            (self.DURABLE, 'Bien Durable'), (self.ENERGIE, 'Energie')]
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
    ELECTRICITE = 'ELECTR'  #énergie domicile
    VETMTS = 'VETMTS'
    DEPLCMT = 'DEPCMT'  #carburant en consommable lavage et entretien en service
    def chx_cat_fnmt(self):
        return [(self.ALIM, 'Alimentation'), (self.ENTRETIEN, 'Entretien'), (self.TOILETTE, 'Toilette'), (self.SANTE, 'Sante'), \
                        (self.ELECTRICITE, 'Electricité'), (self.VETMTS, 'Vetements'), (self.DEPLCMT, 'Deplacement')]
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
    VACANCES = 'VACNC'  # A&M en rando
    VOYAGE = 'VOYAG'   #A&M en visite
    FAMILLE = 'FAMIL' #A&M en famille
    CADEAU = 'CADO'
    def chx_cat_loisir(self):
        return [(self.SPORT, 'Sport'), (self.CULT, 'Culture'), (self.VACANCES, 'Vacances'), \
                (self.VOYAGE,'Voyage'), (self.FAMILLE,'Famille'), (self.CADEAU, 'Cadeaux')]

#DS LE GROUPE PROD
    PATRIM = 'GEST PATRIM'
    SVF = 'SVF'
    TRVX = 'TRVX'
    DECO ='DECO'
    COUTUR = 'COUTUR'
    def chx_cat_prod(self):
        return [(self.PATRIM, 'Patrimoine'), (self.SVF, 'Savoir Faire'), (self.TRVX, 'Travaux/Répar'),
                (self.DECO, 'Decoration'), (self.COUTUR, 'Couture/Tricot')]

    def chx_categorie_achat(self):
        return [(self.FNMT, self.chx_cat_fnmt()), (self.GEST, self.chx_cat_gest()),
                (self.LOISIR, self.chx_cat_loisir()), (self.PROD, self.chx_cat_prod()), ('AUTR', 'Autre ds le groupe') ]

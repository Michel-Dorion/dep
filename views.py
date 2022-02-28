#from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View, generic
from .models import Transaction, Mouvmt_courant, Mouvmt_engage, Achat_ligne, Fournisseur_regulier
from django.contrib.auth.mixins import LoginRequiredMixin
#from dep.forms import AchatForm
#from extra_views import CreateWithInlinesView InlineFormSet
from datetime import datetime, date
#from dep.forms import FournRegTxForm, FournOcasTxForm #echec tentative DRY
#from django.contrib import messages

from dep.module_doc import * #classes de la documentation

# Create your views here.
class DepTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/main.html'
    msg='Bonjour toi'
    def get_context_data(self, **kwargs):
        context = super(DepTemplateView, self).get_context_data(**kwargs)
        context['msg'] = self.msg
        return context

class TxListView(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'dep/txList.html'
    context_object_name = 'tx_list'
    def get_queryset(self):
        qs = super(TxListView, self).get_queryset()
        return qs.order_by('-date_tx')

class TxLivList(LoginRequiredMixin, generic.ListView):
    #liste les tx en attente , soit de livraion, soit de remboursement
    model = Transaction
    template_name = 'dep/txList.html'
    context_object_name = 'tx_list'
    def get_queryset(self):
        qs = super(TxLivList, self).get_queryset()
        qs = qs.filter(nature_tx='LIV') | qs.filter(nature_tx='RBSM')
        qs = qs.order_by('-date_tx')
        print('qs', qs)
        for tx in qs:  # exclure les tx LIV qui ont été intégralement livrées
            engas = Mouvmt_engage.objects.filter(tx_id=tx)
            if tx.nature_tx=='LIV' and not engas : # une tx en attente de livraison prépayée aura un engagmt nul
                #qs.remove(tx) # ne marche pas qs est un queryset
                qs = qs.exclude(pk=tx.id)
        return qs


class TxAbmtRenouvList(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'dep/txList.html'
    context_object_name = 'tx_list'
    def get_queryset(self):
        qs = super(TxAbmtRenouvList, self).get_queryset()
        return qs.filter(nature_tx='ABMT', renouv_auto_tx=True ).order_by('-date_tx')


class TxAbmtPasRenouvList(LoginRequiredMixin, generic.ListView):
    model = Transaction
    template_name = 'dep/txList.html'
    context_object_name = 'tx_list'
    def get_queryset(self):
        qs = super(TxAbmtPasRenouvList, self).get_queryset()
        return qs.filter(nature_tx='ABMT', renouv_auto_tx=False ).order_by('-date_tx')

class TxDetail (LoginRequiredMixin, generic.DetailView) :
    model = Transaction    # transaction is the default context name use in the template
    template_name = 'dep/txDetail.html'
    context_object_name = 'transaction'
    def get_context_data(self, **kwargs):
        context = super(TxDetail, self).get_context_data(**kwargs)
        context['type'] = 'mono'
        return context


class TxRepercut(generic.CreateView):
    model = Transaction
    def repercut_mvmt_fn_nature_tx(self,tx, fourn_reg=None):
        #par nature de tx et selon fourn reg ou fourn occas
        if fourn_reg :
                n_p = fourn_reg.nature_paiemt_hab
                c_b = fourn_reg.compte_bancaire_hab
                m_p = fourn_reg.moyen_paiemt_hab
        if tx.nature_tx == 'UNIT':
            if fourn_reg :
                #print('transaction unitaire', fourn_reg.intitule_tx_hab)
                mvmt = Mouvmt_courant(montant_mvmt=tx.montant_tx, tx_id=tx, date_mvmt = tx.date_tx,
                        nature_paiemt=n_p, compte_bancaire=c_b, moyen_paiemt=m_p )
            else:
                mvmt = Mouvmt_courant(montant_mvmt=tx.montant_tx, tx_id=tx, date_mvmt = tx.date_tx)
            #print('mvmt', mvmt)
            mvmt.save()
        if tx.nature_tx=='LIV':
            # un mouvmt courant si versmt initial

            if tx.versmt_initial != 0 :
                if fourn_reg :
                    mvmt = Mouvmt_courant(montant_mvmt=tx.versmt_initial, tx_id=tx, date_mvmt=tx.date_tx,
                         nature_paiemt=n_p, compte_bancaire=c_b, moyen_paiemt=m_p)
                else :
                     mvmt = Mouvmt_courant(montant_mvmt=tx.versmt_initial, tx_id=tx, date_mvmt=tx.date_tx)
                mvmt.save()
            # un egagmt pour montant tx - versmt initial
            montant_enga = tx.montant_tx - tx.versmt_initial
            if fourn_reg :
                enga = Mouvmt_engage(periode = 'L', tx_id = tx, montant_annonce= montant_enga,
                                        nature_paiemt=n_p, compte_bancaire=c_b, moyen_paiemt=m_p)
            else :
                enga =  Mouvmt_engage(periode = 'L', tx_id = tx, montant_annonce= montant_enga)
            enga.save()


        if tx.nature_tx=='ABMT':
            #print('MDC txeb ANMT', tx)
            if fourn_reg :
                #print('transaction unitaire', fourn_reg.intitule_tx_hab)
                enga = Mouvmt_engage(montant_annonce=tx.montant_tx, tx_id=tx, renouv_auto=tx.renouv_auto_tx,
                        nature_paiemt=n_p, compte_bancaire=c_b, moyen_paiemt=m_p )
            else:
                enga = Mouvmt_engage(tx_id = tx, montant_annonce= tx.montant_tx)
            enga.save()
        return
    def repercut_achat_ligne(self, tx, fourn_reg=None):
        if tx.solo_tx and tx.nature_tx =='UNIT':
            # les tx ABMT solo veront une ligne achat crée à la conv en mvmt courant
            #les tx LIV solo : créer une ligne d'achat à la livraison
            # les tx non solo : lignes d'achat crées manuellement
            if fourn_reg :
                ligne = Achat_ligne(tx_id=tx, montant=tx.montant_tx, date_liv= tx.date_tx, intitule=fourn_reg.intitule_hab,
                    nature_achat=fourn_reg.nature_achat_hab,
                    groupe_achat=fourn_reg.groupe_achat_hab, categorie_achat=fourn_reg.categorie_achat_hab)
            else : #fourn occas création ligne d'achat avec catégorie par défaut à modifier
                ligne = Achat_ligne(tx_id=tx, montant=tx.montant_tx, date_liv= tx.date_tx, intitule=tx.intitule_tx)
            # pas de ligne d'achat pour les tx multi catégories
            ligne.save()
        return

    def get_success_url(self, **kwargs):
        if self.object.nature_tx=='UNIT' :
            # competer le mouvmt courant associe du compte et mode paiement
            return reverse_lazy('dep:txDetail_url', kwargs={'pk': self.object.pk}) #au lieu de txMvmts_url
        #ds les autres cas LIV ou ABMT
        return reverse_lazy('dep:txDetail_url', kwargs={'pk': self.object.pk})


class TxFournEntry(LoginRequiredMixin, TxRepercut):
    # pour un fournisseur régulier
    #model = Transaction    # transaction is the default context name use in the template
    fields = ['date_tx', 'montant_tx',   #'intitule_tx', 'solo_tx', 'nature_tx',  'mode_reglmnt', 'nb_etalmt',
                 'versmt_initial', 'renouv_auto_tx'] #apparaîtront à l'écran de saisie
    def get_context_data(self, **kwargs):
        context = super(TxFournEntry, self).get_context_data(**kwargs)
        context['titre'] = 'pour le fournisseur regulier '
        context['fourn'] = get_object_or_404(Fournisseur_regulier, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        #print('MDC Form valid fourn reg')
        fourn_reg = get_object_or_404(Fournisseur_regulier, pk=self.kwargs['pk'])
        #print('MDC fourn reg intitule ds form_valid', fourn_reg)
        form.instance.fournisseur = fourn_reg.nom_fourn
        #form.instance.date_tx = form.instance.date_tx - timedelta(days=1)
        if form.instance.nature_tx == 'RBSM' :
            form.instance.intitule_tx = 'remboursement'
        else :
            form.instance.intitule_tx = fourn_reg.intitule_tx_hab
        form.instance.solo_tx = fourn_reg.solo_tx_hab
        form.instance.nature_tx = fourn_reg.nature_tx_hab
        #print('MDC form valid : trouve fourn', form.instance.intitule_tx)
        #print('MDC form valid : trouve fourn', fourn_reg)
        #print('form valid pas d1 fourn reg', form)
        tx = form.save(commit='False')

        #print('MDC form valid : traitment du type de tx ')
        super(TxFournEntry, self).repercut_mvmt_fn_nature_tx(tx, fourn_reg)
        super(TxFournEntry, self).repercut_achat_ligne(tx, fourn_reg)

        return super(TxFournEntry, self).form_valid(form)



class TxEntry(LoginRequiredMixin, TxRepercut): # CreateWithInlinesView) :
    # pour un fournisseur occasionnel
    #model = Transaction    # transaction is the default context name use in the template
    #fields = ['fournisseur', 'date_tx', 'intitule_tx','nature_tx', 'renouv_auto_tx', 'montant_tx', 'mode_reglmnt', 'nb_etalmt', 'versmt_initial']
    fields = '__all__'
    def form_valid(self, form):
        #print('MDC Form valid fourn ocas')
        #form.instance.date_tx = form.instance.date_tx - timedelta(days=1)
        tx = form.save(commit='False')
        #print('MDC form valid : traitement du type de tx ', tx)
        super(TxEntry, self).repercut_mvmt_fn_nature_tx(tx)
        #occas_patron = Fournisseur_regulier.objects.filter(nom_fourn='OCCAS PATRON')[0] # query set list
        super(TxEntry, self).repercut_achat_ligne(tx) #pour 1 fourn occas saisie manuelle sauf tx solo
        return super(TxEntry, self).form_valid(form)
        # si tx nature ABMT l'engagmt associe sera auto demande en saisie manuelle
        # ! le montant tx represente des frais d'etbsmt par le recurrent engage



class RepercutMajTx:

    def maj_montant(self, tx, nv_montant, fourn_reg=None):
        if tx.nature_tx=='UNIT' :
            # maj du montant : répersussion mouvmt courant associé
            mvmtFille = Mouvmt_courant.objects.filter(tx_id=tx)[0] #tjrs un mouvmt créé auto
            mvmtFille.montant_mvmt = nv_montant
            mvmtFille.save()
        if tx.solo_tx: #répercussion sur la ligne achat
            achatFille = Achat_ligne.objects.filter(tx_id=tx)[0]
            achatFille.montant = nv_montant
            achatFille.save()

        if tx.nature_tx=='LIV' :
            # si nv montant_tx, maj de l'engagmt associé par delta
            #print('modif montant')
            engaFille = Mouvmt_engage.objects.filter(tx_id=tx)[0]
            engaFille.montant_annonce -= tx.montant_tx - nv_montant
                #si il reste a livrer
            if engaFille.montant_annonce >0: engaFille.save()
                #supp engagmt si tout livre
            else: engaFille.delete()

        #tx ABMT
        if tx.nature_tx=='ABMT':
            # si nv montant_tx, maj de l'engagmt associé au niveau de l'annonce avec mémoire du montant précédent
            engaFille = Mouvmt_engage.objects.filter(tx_id=tx)[0]
            engaFille.montant_precedent = engaFille.montant_annonce
            engaFille.montant_annonce = nv_montant
            engaFille.save()
        return

    def maj_versmt_initial(self, tx, nv_versmt_initial, fourn_reg=None):
        #print('modif versmt initial!')
        #maj du mouvmt courant associé : c le 1° de la liste associe lors de la creation de la tx
            mvmtsFille = Mouvmt_courant.objects.filter(tx_id=tx)  # pas tjrs un mouvmt fille
            if mvmtsFille :
                #si rectif du montant du versmt initial
                if nv_versmt_initial>0 :
                    mvmtsFille[0].montant_mvmt = nv_versmt_initial
                    mvmtsFille[0].save()
                    #si plus de versement initial
                elif nv_versmt_initial==0 :
                    mvmtsFille[0].delete()
                # et s'il n'y en avait pas (versmt initial 0), creation
            else:
                if nv_versmt_initial >0:
                    mvmtFille = Mouvmt_courant(tx_id = tx, montant_mvmt= tx.versmt_initial)
                    mvmtFille.save()
                    # si rectification du versement initial, maj du mouvmt courant associé :
                #c alors le 1° de la liste associe lors de la creation de la tx
            return

    def maj_solo(self, tx, nv_solo, fourn_reg=None):
        #print('bascule solo')
        if nv_solo :
        # si tx devient mono catégorie, création d'une ligne d'achat
            # si la tx concerne un fourn régulier, catégorisation habituelle
            #sinon catégorisation par défaut
            TxRepercut().repercut_achat_ligne(tx, fourn_reg)
            """
            if fourn_reg : #de catégorisation habituelle
                intit = fourn_reg.intitule_hab
                n_a= fourn_reg.nature_achat_hab
                g_a = fourn_reg.groupe_achat_hab
                c_a = fourn_reg.categorie_achat_hab
                achat= Achat_ligne(tx_id=tx, montant=tx.montant_tx, intitule=intit,
                        nature_achat=n_a, groupe_achat=g_a, categorie_achat=c_a)
            else :
                achat = Achat_ligne(tx_id=tx, montant=tx.montant_tx)
            achat.save()
            """
        else : #pas mono catégorie, il faut supprimer la ligne d'achat créée automatiqment pour une tx déclarée mono par erreur
            achats = Achat_ligne.objects.filter(tx_id=tx)
            achats[0].delete()

    def maj_renouv(self, tx, nv_renouv, fourn_reg=None):
        #print ('ds maj_renouv', tx, nv_renouv, fourn_reg)
        # et seulement pour les tx ABMT qui doivent avoir un fourn_reg          
        if (tx.nature_tx == 'ABMT') and fourn_reg :
            # il faut màj l'engagmt associé
            engasFille = Mouvmt_engage.objects.filter(tx_id=tx)
            if engasFille :
                engasFille[0].renouv_auto = nv_renouv
                engasFille[0].save()

        return





class TxUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Transaction
    fields = ['fournisseur', 'date_tx', 'intitule_tx', 'montant_tx', 'nature_tx', 'renouv_auto_tx',
                'mode_reglmnt', 'nb_etalmt', 'versmt_initial', 'solo_tx'] # 'date_tx', non editable
    template_name = 'dep/modif_tx.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txDetail_url', kwargs={'pk': self.object.id})


    def form_valid(self, form):
    #repercussion de la màj d'un mouvmt courant;
        tx = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        # fournisseur régulier
        fourn_reg = Fournisseur_regulier.objects.filter(nom_fourn=tx.fournisseur)
        # màj montant
        if tx.montant_tx!=form.instance.montant_tx :
            RepercutMajTx().maj_montant(tx, form.instance.montant_tx, fourn_reg)
        # màj  versement initial
        if tx.versmt_initial!=form.instance.versmt_initial:
            RepercutMajTx().maj_versmt_initial(tx, form.instance.versmt_initial, fourn_reg)
        #màj indicateur mono catégorie
        if tx.solo_tx!=form.instance.solo_tx:
            RepercutMajTx().maj_solo(tx, form.instance.solo_tx, fourn_reg)
        if tx.renouv_auto_tx!=form.instance.renouv_auto_tx :
            print(tx)
            RepercutMajTx().maj_renouv(tx, form.instance.renouv_auto_tx , fourn_reg) 
        return super(TxUpdate, self).form_valid(form)





class TxDelete(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    fields = '__all__'
    template_name = 'dep/supp_tx.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txList_url')


class TxAchats(LoginRequiredMixin, generic.ListView):
    model = Achat_ligne
    context_object_name = 'achat_list'
    def get_context_data(self, **kwargs):
        context = super(TxAchats, self).get_context_data(**kwargs)
        context['type'] = 'de la transaction'
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        return context
    def get_queryset(self):
        qs = super(TxAchats, self).get_queryset()
        return qs.filter(tx_id=self.kwargs['pk'])

class TxMvmts(LoginRequiredMixin, generic.ListView):
    model = Mouvmt_courant
    context_object_name = 'mvmt_list'
    def get_context_data(self, **kwargs):
        context = super(TxMvmts, self).get_context_data(**kwargs)
        context['type'] = 'de la transaction'
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        return context
    def get_queryset(self):
        qs = super(TxMvmts, self).get_queryset()
        return qs.filter(tx_id=self.kwargs['pk'])


class TxEngas(LoginRequiredMixin, generic.ListView):
    model = Mouvmt_engage
    context_object_name = 'enga_list'
    def get_context_data(self, **kwargs):
        context = super(TxEngas, self).get_context_data(**kwargs)
        context['type'] = 'de la transaction'
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        return context
    def get_queryset(self):
        qs = super(TxEngas, self).get_queryset()
        return qs.filter(tx_id=self.kwargs['pk'])


class MvmtListView(LoginRequiredMixin, generic.ListView):
    model = Mouvmt_courant
    #template_name = 'dep/liste_mouvmt_courant.html'
    def get_queryset(self):
        qs = super(MvmtListView, self).get_queryset()
        #print('order_by_date', qs.order_by('-date_mvmt'))
        return qs.order_by('-date_mvmt')



class MvmtUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Mouvmt_courant
    fields = ['date_mvmt','montant_mvmt', 'nature_paiemt', 'compte_bancaire', 'moyen_paiemt']
    template_name = 'dep/modif_mvmt.html'
    def get_context_data(self, **kwargs):
        context = super(MvmtUpdate, self).get_context_data(**kwargs)
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['tx'])
        return context
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txMvmts_url', kwargs={'pk': self.kwargs['tx']})


class MvmtDetail(LoginRequiredMixin, generic.DetailView) :
    model = Mouvmt_courant

class MvmtEntry(LoginRequiredMixin, generic.CreateView) :
    #saisie manuelle d'un nouveau mouvmt courant pour une tx
    model = Mouvmt_courant
    # tx de fourn reg

    fields = ['date_mvmt', 'nature_paiemt', 'compte_bancaire', 'moyen_paiemt', 'montant_mvmt']
    def get_context_data(self, **kwargs):
        context = super(MvmtEntry, self).get_context_data(**kwargs)
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        return context
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txMvmts_url', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        txMere = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        form.instance.tx_id = txMere
        # si rembsmt montant du mouvmt negatif maj ts mere sauf abonnement
        if form.instance.montant_mvmt < 0 and txMere.nature_tx!='ABMT' : #uniqmt si remboursement
            txMere.montant_tx += form.instance.montant_mvmt
            txMere.save()
        # maj enga associe ds tous les cas
        engasAss = Mouvmt_engage.objects.filter(tx_id=txMere)
        #si il y en a UNIT et LIV entierement facturee n'en ont pas ou plus
        if engasAss and txMere.nature_tx=='LIV' :
            # ABNMT pas concerne
            enga = engasAss[0]
            enga.montant_annonce -= abs(form.instance.montant_mvmt)
            if enga.montant_annonce > 0 : enga.save()
            else : enga.delete()

        return super(MvmtEntry, self).form_valid(form)



class MvmtSoldLiv(LoginRequiredMixin, View):
    #pour la dernière livraison d'une tx LIV, ou pour le dernier àpd la liste des mvmts de cette tx
    def get(self, request, pk):  #pk de la tx
        #print('MDC pk', pk)
        txMere = get_object_or_404(Transaction, pk=pk)
        #print('txMere', txMere)
        #ses mouvmts courants des livraison déjà effectuées
        sesMvmts = Mouvmt_courant.objects.filter(tx_id=txMere.id)
        #print('MDC engas de la tx', sesEngas)
        #calcul du montant du solde
        montant_sold = txMere.montant_tx
        for mvmt in sesMvmts:
            #print('MDC enga de la tx', enga.montant)
            montant_sold -= mvmt.montant_mvmt
        #print('MDC montant solde', montant_sold)
        #pour le dernier mvmt d'une tx UNIT multi categories d'un fournisseur régulier
        if txMere.nature_tx=='LIV' and montant_sold>0 : #pas pls soldes successifs à 0
            solde = Mouvmt_courant(tx_id=txMere, montant_mvmt=montant_sold)
            solde.save()
            #suppression du reste engagé
            sesEngas = Mouvmt_engage.objects.filter(tx_id=txMere.id)
            for enga in sesEngas: #une seul enga attendu du montant restant soldé
                enga.delete()
            return HttpResponseRedirect(reverse_lazy('dep:txMvmtUpdate_url', kwargs={'tx' : txMere.id, 'pk' : solde.id}))
        else :
            return HttpResponseRedirect(reverse_lazy('dep:txMvmts_url', kwargs={'pk' : txMere.id}))


class EngaListView(LoginRequiredMixin, generic.ListView):
    model = Mouvmt_engage
    def get_queryset(self):
        qs = super(EngaListView, self).get_queryset()
        return qs.order_by('jour_ds_periode')
    def get_context_data(self, **kwargs):
        context = super(EngaListView, self).get_context_data(**kwargs)
        context['titre'] = ' '
        return context

class EngaRenouvList(LoginRequiredMixin, generic.ListView):
    model = Mouvmt_engage
    def get_queryset(self):
        qs = super(EngaRenouvList, self).get_queryset().filter(renouv_auto=True)
        return qs.order_by('-tx_id')
    def get_context_data(self, **kwargs):
        context = super(EngaRenouvList, self).get_context_data(**kwargs)
        context['titre'] = ' par les abonnements renouvelables '
        return context


class EngaPrevList(LoginRequiredMixin, generic.ListView):
    model = Mouvmt_engage
    def get_queryset(self):
        qs = super(EngaPrevList, self).get_queryset().filter(renouv_auto=False)
        return qs.order_by('-tx_id')
    def get_context_data(self, **kwargs):
        context = super(EngaPrevList, self).get_context_data(**kwargs)
        context['titre'] = ' par livraison en attente et abmt à renouveler '
        return context

class EngaDetail(LoginRequiredMixin, generic.DetailView) :
    model = Mouvmt_engage

class EngaEntry(LoginRequiredMixin, generic.CreateView) :
    model = Mouvmt_engage
    fields = ['nature_paiemt', 'compte_bancaire', 'moyen_paiemt', 'fin_validite_mp', 'periode', 'jour_ds_periode', 'mois_ds_periode', \
                'montant_precedent', 'montant_annonce', 'effectif_ds_n_periode', 'renouv_auto' ]
    def get_context_data(self, **kwargs):
        context = super(EngaEntry, self).get_context_data(**kwargs)
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        return context
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txDetail_url', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        txMere = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        form.instance.tx_id = txMere
        return super(EngaEntry, self).form_valid(form)


class EngaUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Mouvmt_engage
    fields = ['nature_paiemt', 'compte_bancaire', 'moyen_paiemt', 'fin_validite_mp','periode', 'jour_ds_periode', 'mois_ds_periode', \
                'montant_precedent', 'montant_annonce', 'effectif_ds_n_periode', 'renouv_auto']
    template_name = 'dep/modif_enga.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:engaDetail_url', kwargs={'pk': self.object.id})

class EngaDelete(LoginRequiredMixin, generic.DeleteView):
    model = Mouvmt_engage
    fields = '__all__'
    template_name = 'dep/supp_enga.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:engaList_url')

class RapListView(LoginRequiredMixin, generic.ListView):
    model = Mouvmt_courant
    context_object_name = 'mvmt_list'
    def get_queryset(self):
        #print('rapListView', date_act)
        qs = super(RapListView, self).get_queryset()
        #print('date 1° mvmt', qs[0], qs[0].date_mvmt)
        return qs.filter(rapprochmt_bqe=False, date_mvmt__lte=date.today()).exclude(moyen_paiemt='ESP').order_by('-date_mvmt')
    def get_context_data(self, **kwargs):
        context = super(RapListView, self).get_context_data(**kwargs)
        context['type'] = 'pour rapprochement bancaire'
        return context

class RapBqeMaj(LoginRequiredMixin, generic.UpdateView):
    model = Mouvmt_courant
    fields = '__all__'
    success_url = reverse_lazy('dep:rapList_url')

class RapBqe(LoginRequiredMixin, View):
    def get(self, request, pk):
        m = get_object_or_404(Mouvmt_courant, pk=pk)
        m.rapprochmt_bqe = True
        m.save()
        return HttpResponseRedirect(reverse_lazy('dep:rapList_url'))

class AchatListView(LoginRequiredMixin, generic.ListView):
    model = Achat_ligne
    context_object_name = 'achat_list'
    def get_queryset(self):
        qs = super(AchatListView, self).get_queryset()
        return qs.order_by('-date_liv')


class AchatDetail(LoginRequiredMixin, generic.DetailView):
    model = Achat_ligne

class AchatEntry(LoginRequiredMixin, generic.CreateView):
    model = Achat_ligne
    fields = ['intitule', 'montant', 'nature_achat', 'groupe_achat', 'categorie_achat']
    def get_context_data(self, **kwargs):
        context = super(AchatEntry, self).get_context_data(**kwargs)
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        return context
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txAchats_url', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        txMere = get_object_or_404(Transaction, pk=self.kwargs['pk'])
        form.instance.tx_id = txMere
        if txMere.solo_tx :
            form.instance.montant = txMere.montant_tx
            form.instance.intitule = txMere.intitule_tx
        return super(AchatEntry, self).form_valid(form)



class AchatSold(LoginRequiredMixin, View):
    def get(self, request, pk):
        #print('MDC pk', pk),
        txMere = get_object_or_404(Transaction, pk=pk)
        #tx Mère LIV (avec solde)
        #print('txMere', txMere)
        sesLignesAchat =  Achat_ligne.objects.filter(tx_id=txMere.id)
        #print('MDC engas de la tx', sesEngas)
        #calcul du montant restant
        montant_sold = txMere.montant_tx
        for ligne in sesLignesAchat :
            montant_sold -= ligne.montant
        #si solde nul  envoi msg 'solde dèjà nul'
        if montant_sold==0:
            return HttpResponseRedirect(reverse_lazy('dep:txAchats_url', kwargs={'pk' : txMere.id}))
        # remonter au fournisseur
        fourn_reg = Fournisseur_regulier.objects.filter(nom_fourn=txMere.fournisseur)
        if fourn_reg :
            int = fourn_reg[0].intitule_tx_hab
            nat = fourn_reg[0].nature_achat_hab
            gra = fourn_reg[0].groupe_achat_hab
            cat = fourn_reg[0].categorie_achat_hab
            #print('achat sold intitulé, nature, groupe, catégorie habituelles : ', int, nat, gra, cat)
            solde = Achat_ligne(tx_id=txMere, intitule= int, nature_achat=nat, groupe_achat=gra, categorie_achat=cat, montant=montant_sold)
        else:
            int='fourn occas' #sinon fournisseur occas
            solde = Achat_ligne(tx_id=txMere, intitule= int, montant=montant_sold)
        solde.save()
        return HttpResponseRedirect(reverse_lazy('dep:txAchatUpdate_url', kwargs={'tx' : txMere.id, 'pk' : solde.id}))



class AchatUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Achat_ligne
    fields = ['intitule', 'date_liv', 'montant', 'nature_achat', 'groupe_achat', 'categorie_achat']
    template_name = 'dep/modif_achat_ligne.html'
    def get_context_data(self, **kwargs):
        context = super(AchatUpdate, self).get_context_data(**kwargs)
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['tx'])
        return context
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txAchats_url', kwargs={'pk': self.kwargs['tx']})

class AchatDelete(LoginRequiredMixin, generic.DeleteView):
    model = Achat_ligne
    fields = '__all__'
    template_name = 'dep/supp_achat_ligne.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:txAchats_url', kwargs={'pk': self.kwargs['tx']})
    def get_context_data(self, **kwargs):
        context = super(AchatDelete, self).get_context_data(**kwargs)
        context['tx_id'] = get_object_or_404(Transaction, pk=self.kwargs['tx'])
        return context



class EngaConv(LoginRequiredMixin, View):

    def ajout_mvmt(self, enga, hdt_act): # ajout d1 mouvmt courant sur ordre de conversion d1 mouvmt engage
        #print('ds ajout_mvmt', enga)
        #print('hdt_act', hdt_act, hdt_act.month)
        if enga.periode=='L' :
            j_paiemt= hdt_act.day
        else : #ABMT
            if enga.renouv_auto :
                j_paiemt = enga.jour_ds_periode
                #print('periode', enga.periode, j_paiemt)
                if j_paiemt==0:  # 0 par defaut indique sais pas alors que 1 indique que c'est 1e premier j du mois
                    j_paiemt= 1
            else : # abmt à renouv manuel
                j_paiemt =  hdt_act.day

        #print('contruction dt_paiemt : mois et jour', hdt_act.month, j_paiemt)
        dt_paiemt = date(hdt_act.year, hdt_act.month, j_paiemt) #il verifie la limite du jour pour le mois
        #print('dt_paiemt', dt_paiemt)
        tx = enga.tx_id
        n_p = enga.nature_paiemt
        m_p = enga.moyen_paiemt
        mt = enga.montant_annonce
        m = Mouvmt_courant(tx_id=tx , nature_paiemt=n_p, moyen_paiemt=m_p, montant_mvmt=mt, date_mvmt=dt_paiemt)
        #print('nv mvmt courant', m)
        m.save()
        # et ligne achat correpondante pour les abmts
        if tx.nature_tx=='ABMT':  #ts les abmts sont supposé solo en catégorie d'achat
            #print('dans conv ligne achat')
            #retrouver le fournisseur
            fourn_reg = Fournisseur_regulier.objects.filter(nom_fourn=tx.fournisseur)
            if fourn_reg:
                #print('fourn_reg', fourn_reg)
                intitule = fourn_reg[0].intitule_hab
                n_a = fourn_reg[0].nature_achat_hab
                g_a = fourn_reg[0].groupe_achat_hab
                c_a = fourn_reg[0].categorie_achat_hab
                #print('categorie achat pour abmt', c_a)

                a = Achat_ligne(tx_id=tx, intitule = intitule, montant=tx.montant_tx,
                                    nature_achat=n_a, groupe_achat=g_a, categorie_achat=c_a )
                a.save()
        # maj de l'engagmt
        enga.horodate_dern_conv = datetime.now()
        enga.save()
        return

    def conv(self, engagmts):  #conversion d1 liste d'engagmts
        hdt_act = datetime.now()
        mois_act = hdt_act.month
        #un_mois = timedelta(days=30)
        #print('ds conv', mois_act)
        for enga in engagmts :
            #print('enga ds conv', enga)
            if (enga.periode=='M' and (not enga.horodate_dern_conv or enga.horodate_dern_conv.month<mois_act)):
                # abnmt mensuel pour lesquels soit il n'y pas encore eu de conversion, soit elle a deja ete faite pour la periode
                #print('selction pour les abmt mensuels', enga)
                if enga.effectif_ds_n_periode>0:
                    print('n_periode>0')
                    enga.effectif_ds_n_periode -=1 #pas pour cette fois
                    enga.horodate_dern_conv = datetime.now()
                    enga.save()
                else:
                    #print('ajout mvmt courant')
                    self.ajout_mvmt(enga, hdt_act)
            if (enga.periode=='L' and (not enga.horodate_dern_conv or enga.horodate_dern_conv.month<mois_act)):
                # facturation a la livraison
                if enga.montant_annonce != 0 : # on ne convertit pas les cdes prépayées dont on attend la livraison
                    self.ajout_mvmt(enga, hdt_act)
                    enga.delete()
            if (enga.periode=='A' and (not enga.horodate_dern_conv or enga.horodate_dern_conv.month<mois_act)):
                    if enga.mois_ds_periode==mois_act:
                        print('ajout mvmt courant annuel')
                        self.ajout_mvmt(enga, hdt_act)
            if (enga.periode=='S' and (not enga.horodate_dern_conv or enga.horodate_dern_conv.month<mois_act)):
                    if (enga.mois_ds_periode==mois_act or enga.mois_ds_periode==(mois_act+6)%12) :
                        print('ajout mvmt courant annuel')
                        self.ajout_mvmt(enga, hdt_act)
            #break  pour les essais
                #depuis_dern_conv = hdt_now - enga.horodate_dern_conv
                #if enga.periode=='M' and depuis_dern_conv>=un_mois :
                #if not enga.horodate_dern_conv : pas_rept = True
                #elsif enga.horodate_dern_conv.month<mois_act : pas_rept = True
        return



    def get(self, request, pk=0):
        #distinguer entre conv chgmt de periode et conv specifiq d1 engamt selon présence du parm pk
        #print('MDC request', request)
        if pk==0:   # nvlle periode pour les renouvellements automatiques
            #print('nvlle periode')
            engagmts = Mouvmt_engage.objects.all().filter(renouv_auto=True)
            #print('MDC nb de mvmts engage', len(engagmts))
            self.conv(engagmts)
            return HttpResponseRedirect(reverse_lazy('dep:rapList_url'))
        else: # abmt sans renouv auto ou livraison
            #print("conv pour l'enga", pk)
            engagmts = [get_object_or_404(Mouvmt_engage, pk=pk)]
            self.conv(engagmts)
            return HttpResponseRedirect(reverse_lazy('dep:engaList_url'))


class FournListView(LoginRequiredMixin, generic.ListView): # LoginRequiredMixin en 1° pos sinon perte de la fn
    model = Fournisseur_regulier
    context_object_name = 'fourn_list'
    def get_queryset(self):
        qs = super(FournListView, self).get_queryset()
        return qs.order_by('nom_fourn')

class FournRegListView(FournListView):
    # pour la liste des fourn reg hors abmt
    def get_queryset(self):
        qs = super(FournRegListView, self).get_queryset()
        return qs.exclude(nature_tx_hab='ABMT').order_by('nom_fourn')

class FournAbmtListView(FournListView):  # pas LoginRequiredMixin sinon viol MRO : inutile puisq hérité
    # pour la liste des fourn par abmt
    def get_queryset(self):
        qs = super(FournAbmtListView, self).get_queryset()
        return qs.filter(nature_tx_hab='ABMT').order_by('nom_fourn')

class FournDetail(LoginRequiredMixin, generic.DetailView):
    model = Fournisseur_regulier


class FournEntry(LoginRequiredMixin, generic.CreateView):
    model = Fournisseur_regulier
    fields = '__all__'
    success_url = reverse_lazy('dep:fournList_url')

class FournUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Fournisseur_regulier
    fields = '__all__'
    template_name = 'dep/modif_fourn.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:fournDetail_url', kwargs={'pk': self.object.id})


class FournDelete(LoginRequiredMixin, generic.DeleteView):
    model = Fournisseur_regulier
    fields = '__all__'
    template_name = 'dep/supp_fourn.html'
    def get_success_url(self, **kwargs):
        return reverse_lazy('dep:fournList_url')





















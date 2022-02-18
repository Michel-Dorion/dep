from django.urls import path


from .views import DepTemplateView, \
        DepDocTemplateView,  DepDocPresgen, DepDocTxFournOccas, DepDocTxFournReg, DepDocModifTx, DepDocCasdusage, DepDocRembsmt,DepDocModeles, \
        TxListView, TxAbmtRenouvList, TxAbmtPasRenouvList, TxLivList, TxDetail, \
        TxEntry, TxUpdate, TxDelete,TxAchats, TxMvmts, TxEngas,  TxFournEntry, \
        MvmtListView, MvmtDetail, MvmtEntry, MvmtUpdate, MvmtSoldLiv, \
        EngaListView, EngaDetail, EngaEntry, EngaUpdate, EngaConv, EngaRenouvList, EngaPrevList, EngaDelete, \
        RapListView, RapBqe, \
        AchatListView, AchatDetail, AchatEntry, AchatUpdate, AchatDelete, AchatSold, \
        FournListView, FournRegListView, FournAbmtListView, FournDetail, FournEntry, FournUpdate, FournDelete


app_name = 'dep'
urlpatterns = [
    path('', DepTemplateView.as_view(), name='dep_url'),
    path('doc/', DepDocTemplateView.as_view(), name='depDoc_url'),
    path('docPresgen/', DepDocPresgen.as_view(), name='docPresgen_url'),
    path('docTxFournOccas/', DepDocTxFournOccas.as_view(), name='docTxFournOccas_url'),
    path('docTxFournReg/', DepDocTxFournReg.as_view(), name='docTxFournReg_url'),
    path('docModifTx/', DepDocModifTx.as_view(), name='docModifTx_url'),
    path('docCasdusage/', DepDocCasdusage.as_view(), name='docCasdusage_url'),
    path('docRembsmt/', DepDocRembsmt.as_view(), name='docRembsmt_url'),
    path('docModeles/', DepDocModeles.as_view(), name='docModeles_url'),
    path('tx/', TxListView.as_view(template_name='dep/txList.html', context_object_name='tx_list'), name='txList_url'),
    path('tx/abmtrenouv', TxAbmtRenouvList.as_view(template_name='dep/txList.html', context_object_name='tx_list'), name='txAbmtRenouvList_url'),
    path('tx/abmtpasrenouv', TxAbmtPasRenouvList.as_view(template_name='dep/txList.html', context_object_name='tx_list'), name='txAbmtPasRenouvList_url'),
    path('tx/liv', TxLivList.as_view(template_name='dep/txList.html', context_object_name='tx_list'), name='txLivList_url'),
    path('tx/<int:pk>/', TxDetail.as_view(template_name='dep/txDetail.html'), name='txDetail_url'), #context transaction
    path('txen/', TxEntry.as_view(), name='txEntry_url'),
    path('txupdate/<int:pk>/', TxUpdate.as_view(), name='txUpdate_url'),
    path('txdelete/<int:pk>/', TxDelete.as_view(), name='txDelete_url'),
    path('txachats/<int:pk>/', TxAchats.as_view(template_name='dep/achatList.html'), name='txAchats_url'),
    path('txachats/<int:tx>/update/<int:pk>', AchatUpdate.as_view(), name='txAchatUpdate_url'),
    path('txachats/<int:tx>/delete/<int:pk>', AchatDelete.as_view(), name='txAchatDelete_url'),
    path('txachaten/<int:pk>/', AchatEntry.as_view(), name='txNvligne_url'),   #création achat pour cette tx
    path('txengas/<int:pk>/', TxEngas.as_view(template_name='dep/engaList.html'), name='txEngas_url'),
    path('txenga/<int:tx>/update/<int:pk>', EngaUpdate.as_view(), name='txEngaUpdate_url'),
    path('txmvmts/<int:pk>/', TxMvmts.as_view(template_name='dep/mvmtList.html'), name='txMvmts_url'), #liste des mvmts d1 tx
    path('txmvmt/<int:tx>/update/<int:pk>', MvmtUpdate.as_view(), name='txMvmtUpdate_url'),
    path('txmvmten/<int:pk>>', MvmtEntry.as_view(), name='txNvmvmt_url'),  #création mvmt pour cette tx
    path('txmvmts/<int:tx>/update/<int:pk>', MvmtUpdate.as_view(), name='txMvmtUpdate_url'),
    path('txengaen/<int:pk>>', EngaEntry.as_view(), name='txNvenga_url'),

    #
    path('mvmt/', MvmtListView.as_view(template_name='dep/mvmtList.html', context_object_name='mvmt_list'), name='mvmtList_url'),
    path('mvmt/<int:pk>', MvmtDetail.as_view(template_name='dep/mvmtDetail.html'), name='mvmtDetail_url'),
    path('mvmten/', MvmtEntry.as_view(), name='mvmtEntry_url'),
    path('mvmtupdt/<int:pk>', MvmtUpdate.as_view(), name='mvmtUpdate_url'), #màj d1 mvmt d'une tx
    path('mvmtsoldliv/<int:pk>', MvmtSoldLiv.as_view(), name='mvmtSoldLiv_url'),
    #
    path('rapbqe/', RapListView.as_view(template_name='dep/mvmtList.html'), name='rapList_url'),
    path('rapbqe/<int:pk>/', RapBqe.as_view(), name='rapBqe_url'),
    #

    path('enga/', EngaListView.as_view(template_name='dep/engaList.html', context_object_name='enga_list'), name='engaList_url'),
    path('engarenouv/', EngaRenouvList.as_view(template_name='dep/engaList.html', context_object_name='enga_list'), name='engaRenouvList_url'),
    path('engaprev/', EngaPrevList.as_view(template_name='dep/engaList.html', context_object_name='enga_list'), name='engaPrevList_url'),
    path('enga/<int:pk>/', EngaDetail.as_view(template_name='dep/engaDetail.html'), name='engaDetail_url'),
    path('engaen/', EngaEntry.as_view(), name='engaEntry_url'),
    path('engaupdate/<int:pk>/', EngaUpdate.as_view(template_name='dep/modif_enga.html'), name='engaUpdate_url'),
    path('engaconv/', EngaConv.as_view(), name='engasConv_url'),
    path('engaconvunit/<int:pk>/', EngaConv.as_view(), name='engaConv_url'),
    path('engadel/<int:pk>/', EngaDelete.as_view(), name='engaDelete_url'),
    #
    path('achat/', AchatListView.as_view(template_name='dep/achatList.html'), name='achatList_url'),
    path('achat/<int:pk>', AchatDetail.as_view(template_name='dep/achatDetail.html'), name='achatDetail_url'),
    path('achaten/', AchatEntry.as_view(), name='achatEntry_url'),
    path('achatupdt/<int:pk>', AchatUpdate.as_view(), name='achatUpdate_url'),
    path('achatsold/<int:pk>', AchatSold.as_view(), name='achatSold_url'),   #creation d'une ligne les articles habiturels d'1 fournisseur rég

    path('fourn/', FournListView.as_view(template_name='dep/fournList.html'), name='fournList_url'),
    path('fournreg/', FournRegListView.as_view(template_name='dep/fournList.html'), name='fournRegList_url'),
    path('fournabmt/', FournAbmtListView.as_view(template_name='dep/fournList.html'), name='fournAbmtList_url'),
    path('fourn/<int:pk>', FournDetail.as_view(template_name='dep/fournDetail.html'), name='fournDetail_url'),
    path('fournen/', FournEntry.as_view(), name='fournEntry_url'),
    path('fournupd/<int:pk>/', FournUpdate.as_view(), name='fournUpdate_url'),
    path('fourndel/<int:pk>/', FournDelete.as_view(), name='fournDelete_url'),
    path('fourntxen/<int:pk>', TxFournEntry.as_view(), name='fournNvltx_url'),

    ]




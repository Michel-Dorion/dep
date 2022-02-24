# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic



class DepDocTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/depDoc.html'

class  DepDocPresgen(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/docPresgen.html'

class DepDocTxFournOccas(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/docTxFournOccas.html'

class DepDocTxFournReg(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/docTxFournReg.html'

class DepDocModifTx(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/docModifTx.html'

class DepDocCasdusage(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/docCasdusage.html'

class DepDocRembsmt(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/docRembsmt.html'

class DepDocModeles(LoginRequiredMixin, generic.TemplateView):
    template_name='dep/docModeles.html'
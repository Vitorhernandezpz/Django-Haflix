from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from .models import Filme
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.
class Homepage(TemplateView):
    template_name = "homepage.html"

class Homefilmes(ListView):
    template_name = "homefilmes.html"
    model = Filme

class Detalhesfilmes(DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        return super().get(request, *args, **kwargs) # Redireciona o usuario para a url final

    # super executa a função da super classe, no caso a detailview
    def get_context_data(self, **kwargs):
        context = super(Detalhesfilmes, self).get_context_data()
        # filtrar a minha tabela de filmes pegando os filmes cuja categoria é igual a categoria do filme da página (object)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context

class Pesquisafilme(ListView):
    template_name = "pesquisa.html"
    model = Filme

    # Edição do object_list
    # Função para pegar o valor digitado na barra de pesquisa e retorna todos os filmes que contem o termo pesquisado que foi digitado na barra de pesquisa
    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

#def homepage(request):
#    return render(request,'homepage.html')

# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request,"homefilmes.html", context)
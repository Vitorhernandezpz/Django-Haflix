from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormHomepage

# Create your views here.
class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
       if request.user.is_authenticated:
           return redirect('filme:homefilmes')
       else:
        return super().get(request, *args, **kwargs) # Redireciona para homepage, caso user não está autenticado

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse("filme:login")
        else:
            return reverse("filme:criarconta")

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme

class Detalhesfilmes(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        # Adicionando no banco o filme visto para o usuario de forma dinamica
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) # Redireciona o usuario para a url final

    # super executa a função da super classe, no caso a detailview
    def get_context_data(self, **kwargs):
        context = super(Detalhesfilmes, self).get_context_data()
        # filtrar a minha tabela de filmes pegando os filmes cuja categoria é igual a categoria do filme da página (object)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context

class Pesquisafilme(LoginRequiredMixin, ListView):
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

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    # Campos que serão atualizados de acordo com o modelo do AbstractUser
    fields = ['first_name','last_name','email']

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm


    # Função que verifica se o formulario é valido, se todos os campos do form foram preenchidos e salva o form para criar o usuário no banco
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # Função espera um link como resposta e não um redirect
    def get_success_url(self):
        return reverse("filme:login")

#def homepage(request):
#    return render(request,'homepage.html')

# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request,"homefilmes.html", context)
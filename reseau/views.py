from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView
from .form import CreationForm, CommentaireForm
from .models import Contenu, Commentaire
# Create your views here.

class Connexion(LoginView):
    form_class = AuthenticationForm
    template_name = 'reseau/Login.html'
    redirect_authenticated_user = True
    next = "liste"


def creation_utilisateur(request):
    form = CreationForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        verify_password = form.cleaned_data['verify_password']
        envoi = True
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            messages.add_message(request, messages.INFO, "Erreur Login déja présent")
            return render(request, 'reseau/creation.html', locals())
        messages.add_message(request, messages.INFO, "compte créé connectez-vous")
        return redirect('login')
    return render(request, 'reseau/creation.html', locals())

def admin(request):
    return redirect('admin1')


def deconnexion(request):
    logout(request)
    return redirect('login')


class ListUser(LoginRequiredMixin, ListView):
    login_url = '/reseau/'
    model = User
    context_object_name = "liste_user"
    template_name = "reseau/liste.html"

@login_required
def view_user(request, pk):
    utilisateur = User.objects.get(id=pk)
    form = CommentaireForm(request.POST or None)

    if form.is_valid():
        texte = form.cleaned_data['texte']
        commentaire_parent = int(form.cleaned_data['commentaire_parent'])
        createur = request.user
        profil_cible = utilisateur
        if commentaire_parent ==0:
            if createur == profil_cible:
                Contenu.objects.create(profil_cible=profil_cible, texte=texte, createur=createur, mode= 1)
                messages.add_message(request, messages.INFO, "Statut posté")
            elif createur != profil_cible:
                Contenu.objects.create(profil_cible=profil_cible, texte=texte, createur=createur, mode = 2)
                messages.add_message(request, messages.INFO, "message envoyé")
        elif commentaire_parent !=0:
            print("test")
            s=Contenu.objects.get(pk=commentaire_parent)
            Commentaire.objects.create(profil_cible=profil_cible, texte= texte,createur=createur, mode=3,commentaire_parent=s)
            messages.add_message(request, messages.INFO, "commentaire posté")
        envoi = True

    statut_messages = Contenu.objects.filter(profil_cible=pk).filter(Q(mode=1) | Q(mode=2)).order_by('-date')
    commentaires = Commentaire.objects.filter(Q(profil_cible=pk)).order_by('-commentaire_parent').order_by('date')
    return render(request, "reseau/detail_user.html", locals())


# @login_required
# class DetailUser(DetailView):
#     model = User
#     context_object_name = "utilisateur"
#     template_name = "reseau/detail_user.html"
statut_messages = Contenu.objects.filter(Q(profil_cible=1), Q(mode=2)).order_by('-date')

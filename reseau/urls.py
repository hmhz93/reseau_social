from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.Connexion.as_view(), name='login'),
    path('creation/', views.creation_utilisateur, name='creation_utilisateur'),
    path('admin/', views.admin, name='admin'),
    path('deconnexion/', views.deconnexion, name = 'deconnexion'),
    path('liste/', views.ListUser.as_view(), name='liste'),
    re_path(r'^detail/(?P<pk>\d+)', views.view_user, name='detail'),
]

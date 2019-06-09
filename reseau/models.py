from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# Create your models here.


class Contenu(models.Model):
    profil_cible = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createur")
    texte = models.TextField()
    date = models.DateTimeField(default=timezone.now, verbose_name="Date de Parution")
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cible")
    # mode 1 statut, 2 message, 3 commentaire
    mode = models.IntegerField()
    # level = models.IntegerField()

    class Meta:
        verbose_name = "Contenu"

    def __str__(self):
        return "{} - {}".format(self.profil_cible, self.texte[:10])


class Commentaire(Contenu):
    commentaire_parent = models.ForeignKey('Contenu', on_delete=models.CASCADE, null=True, related_name="Parent")


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement un profil pour chaque nouvel utilisateur.
    """
    if created:
        # Crée le profil uniquement si l'utilisateur vient d'être créé
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     """
#     Sauvegarde le profil existant lors de la sauvegarde de l'utilisateur.
#     """
#     try:
#         instance.profile.save()
#     except Profile.DoesNotExist:
#         # Si jamais il n'existe pas (cas rare), on le crée
#         Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # Crée un profil si l'utilisateur est nouveau
        Profile.objects.get_or_create(user=instance)
    # else:
    #     # Met à jour le profil seulement s'il existe
    #     try:
        instance.profile.save()
        # except Profile.DoesNotExist:
        #     # Ignore si le profil n'existe pas
        #     pass
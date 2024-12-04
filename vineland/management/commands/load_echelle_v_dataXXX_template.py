from django.core.management.base import BaseCommand
from django.db import transaction
from polls.models import SousDomain
from vineland.models import EchelleVMapping

class Command(BaseCommand):
    help = 'Charge les données de conversion échelle-V pour la tranche d\'âge 1:0:0-1:0:30'

    def handle(self, *args, **kwargs):
        # Données de mapping pour la tranche d'âge 1:0:0-1:0:30
        mappings_data = {
            'Réceptive': [],
            'Expressive': [],
            'Écrite': [],
            'Personnelle': [],
            'Domestique': [],
            'Communautaire': [],
            'Relations interpersonnelles': [],
            'Jeu et temps libre': [],
            'Adaptation': [],
            'Globale': [],
            'Fine': [],
        }

        age_debut_annee_value = 1
        age_debut_mois_value = 0
        age_debut_jour_value = 0

        age_fin_annee_value = 1
        age_fin_mois_value = 0
        age_fin_jour_value = 30

        try:
            with transaction.atomic():
                # Supprimer les anciennes données pour cette tranche d'âge
                EchelleVMapping.objects.filter(
                    age_debut_annee= age_debut_annee_value,
                    age_debut_mois= age_debut_mois_value,
                    age_debut_jour= age_debut_jour_value,
                    age_fin_annee= age_fin_annee_value,
                    age_fin_mois= age_fin_mois_value,
                    age_fin_jour= age_fin_jour_value
                ).delete()

                # Charger les nouvelles données
                for sous_domaine_name, mappings in mappings_data.items():
                    try:
                        sous_domaine = SousDomain.objects.get(name=sous_domaine_name)
                        self.stdout.write(f"Traitement du sous-domaine: {sous_domaine_name}")
                        
                        for mapping in mappings:
                            EchelleVMapping.objects.create(
                                sous_domaine=sous_domaine,
                                age_debut_annee= age_debut_annee_value,
                                age_debut_mois= age_debut_mois_value,
                                age_debut_jour= age_debut_jour_value,
                                age_fin_annee= age_fin_annee_value,
                                age_fin_mois= age_fin_mois_value,
                                age_fin_jour= age_fin_jour_value,
                                note_brute_min=mapping['min'],
                                note_brute_max=mapping['max'],
                                note_echelle_v=mapping['v']
                            )
                        
                        self.stdout.write(self.style.SUCCESS(
                            f'Données chargées pour {sous_domaine_name}'
                        ))
                            
                    except SousDomain.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f'Sous-domaine non trouvé: {sous_domaine_name}'
                        ))
                        continue

                self.stdout.write(self.style.SUCCESS(
                    'Toutes les données échelle-V ont été chargées avec succès '
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Erreur lors du chargement des données: {str(e)}'
            ))
            raise
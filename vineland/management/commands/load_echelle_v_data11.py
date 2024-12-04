from django.core.management.base import BaseCommand
from django.db import transaction
from polls.models import SousDomain
from vineland.models import EchelleVMapping

class Command(BaseCommand):
    help = 'Charge les données de conversion échelle-V pour la tranche d\'âge 1:0:0-1:0:30'

    def handle(self, *args, **kwargs):
        # Données de mapping pour la tranche d'âge 1:0:0-1:0:30
        mappings_data = {
            'Réceptive': [
                {'min': 19, 'max': 40, 'v': 24},
                {'min': 18, 'max': 18, 'v': 23},
                {'min': 17, 'max': 17, 'v': 22},
                {'min': 16, 'max': 16, 'v': 21},
                {'min': 15, 'max': 15, 'v': 20},
                {'min': 14, 'max': 14, 'v': 19},
                {'min': 13, 'max': 13, 'v': 18},
                {'min': 12, 'max': 12, 'v': 17},
                {'min': 11, 'max': 11, 'v': 16},
                {'min': 10, 'max': 10, 'v': 15},
                {'min': 9, 'max': 9, 'v': 14},
                {'min': 8, 'max': 8, 'v': 13},
                {'min': 7, 'max': 7, 'v': 12},
                {'min': 6, 'max': 6, 'v': 11},
                {'min': 5, 'max': 5, 'v': 10},
                {'min': 4, 'max': 4, 'v': 8},
                {'min': 3, 'max': 3, 'v': 7},
                {'min': 2, 'max': 2, 'v': 6},
                {'min': 1, 'max': 1, 'v': 4},
                {'min': 0, 'max': 0, 'v': 3},
            ],
            'Expressive': [
                {'min': 27, 'max': 108, 'v': 24},
                {'min': 26, 'max': 26, 'v': 23},
                {'min': 25, 'max': 25, 'v': 22},
                {'min': 24, 'max': 24, 'v': 21},
                {'min': 22, 'max': 23, 'v': 20},
                {'min': 21, 'max': 21, 'v': 19},
                {'min': 20, 'max': 20, 'v': 18},
                {'min': 19, 'max': 19, 'v': 17},
                {'min': 18, 'max': 18, 'v': 16},
                {'min': 16, 'max': 17, 'v': 15},
                {'min': 15, 'max': 15, 'v': 14},
                {'min': 14, 'max': 14, 'v': 13},
                {'min': 13, 'max': 13, 'v': 12},
                {'min': 11, 'max': 12, 'v': 11},
                {'min': 10, 'max': 10, 'v': 10},
                {'min': 8, 'max': 9, 'v': 9},
                {'min': 6, 'max': 7, 'v': 8},
                {'min': 3, 'max': 5, 'v': 7},
                {'min': 0, 'max': 2, 'v': 6},
            ],
            'Écrite': [
                {'min': 0, 'max': 0, 'v': 1},  # Pas de données dans l'image, valeur par défaut
            ],
            'Personnelle': [
                {'min': 21, 'max': 82, 'v': 24},
                {'min': 19, 'max': 20, 'v': 23},
                {'min': 17, 'max': 18, 'v': 22},
                {'min': 16, 'max': 16, 'v': 21},
                {'min': 14, 'max': 15, 'v': 20},
                {'min': 13, 'max': 13, 'v': 19},
                {'min': 11, 'max': 12, 'v': 18},
                {'min': 10, 'max': 10, 'v': 17},
                {'min': 9, 'max': 9, 'v': 16},
                {'min': 7, 'max': 8, 'v': 15},
                {'min': 6, 'max': 6, 'v': 14},
                {'min': 5, 'max': 5, 'v': 13},
                {'min': 4, 'max': 4, 'v': 12},
                {'min': 3, 'max': 3, 'v': 11},
                {'min': 2, 'max': 2, 'v': 9},
                {'min': 1, 'max': 1, 'v': 7},
                {'min': 0, 'max': 0, 'v': 6},
            ],
            'Domestique': [
                {'min': 8, 'max': 48, 'v': 24},
                {'min': 6, 'max': 7, 'v': 23},
                {'min': 5, 'max': 5, 'v': 22},
                {'min': 4, 'max': 4, 'v': 20},
                {'min': 3, 'max': 3, 'v': 19},
                {'min': 2, 'max': 2, 'v': 18},
                {'min': 1, 'max': 1, 'v': 17},
                {'min': 0, 'max': 0, 'v': 15},
            ],
            'Communautaire': [
                {'min': 7, 'max': 88, 'v': 24},
                {'min': 6, 'max': 6, 'v': 23},
                {'min': 5, 'max': 5, 'v': 22},
                {'min': 4, 'max': 4, 'v': 20},
                {'min': 3, 'max': 3, 'v': 18},
                {'min': 2, 'max': 2, 'v': 16},
                {'min': 1, 'max': 1, 'v': 14},
                {'min': 0, 'max': 0, 'v': 13},
            ],
            'Relations interpersonnelles': [
                {'min': 35, 'max': 76, 'v': 24},
                {'min': 34, 'max': 34 , 'v': 23},
                {'min': 32, 'max': 33, 'v': 22},
                {'min': 31, 'max':31 , 'v': 21},
                {'min': 29, 'max': 30, 'v': 20},
                {'min': 28, 'max': 28 , 'v': 19},
                {'min': 26, 'max': 27, 'v': 18},
                {'min': 25, 'max': 25 , 'v': 17},
                {'min': 23, 'max': 24, 'v': 16},
                {'min': 22, 'max':22 , 'v': 15},
                {'min': 21, 'max': 21, 'v': 14},
                {'min': 19, 'max': 20 , 'v': 13},
                {'min': 18, 'max':18 , 'v': 12},
                {'min': 17, 'max': 17, 'v': 11},
                {'min':16 , 'max':16 , 'v': 10},
                {'min':15 , 'max':15 , 'v': 9},
                {'min':13 , 'max':14 , 'v': 8},
                {'min':12 , 'max': 12, 'v': 7},
                {'min':11 , 'max': 11, 'v': 6},
                {'min':10 , 'max':10 , 'v': 5},
                {'min':9 , 'max': 9, 'v': 4},
                {'min':8 , 'max':8 , 'v': 3},
                {'min': 7 , 'max':  7, 'v': 2},
                {'min': 0, 'max': 6 , 'v': 1},
            ],
            'Jeu et temps libre': [
                {'min': 22, 'max': 62, 'v': 24},
                {'min': 21, 'max': 21, 'v': 23},
                {'min': 19, 'max': 20, 'v': 22},
                {'min': 18, 'max': 18, 'v': 21},
                {'min': 17, 'max': 17, 'v': 20},
                {'min': 15, 'max': 16, 'v': 19},
                {'min': 14, 'max': 14, 'v': 18},
                {'min': 13, 'max': 13, 'v': 17},
                {'min': 12, 'max': 12, 'v': 16},
                {'min': 10, 'max': 11, 'v': 15},
                {'min': 9, 'max': 9, 'v': 14},
                {'min': 7, 'max': 8, 'v': 13},
                {'min': 6, 'max': 6, 'v': 12},
                {'min': 5, 'max': 5, 'v': 11},
                {'min': 3, 'max': 4, 'v': 10},
                {'min': 2, 'max': 2, 'v': 9},
                {'min': 0, 'max': 1, 'v': 8},
            ],
            'Adaptation': [
                {'min': 10, 'max': 60, 'v': 24},
                {'min': 9, 'max': 9, 'v': 23},
                {'min': 8, 'max': 8, 'v': 22},
                {'min': 7, 'max': 7, 'v': 21},
                {'min': 6, 'max': 6, 'v': 20},
                {'min': 5, 'max': 5, 'v': 18},
                {'min': 4, 'max': 4, 'v': 17},
                {'min': 3, 'max': 3, 'v': 15},
                {'min': 2, 'max': 2, 'v': 14},
                {'min': 1, 'max': 1, 'v': 12},
                {'min': 0, 'max': 0, 'v': 11},
            ],
            'Globale': [
                {'min': 49, 'max': 80, 'v': 24},
                {'min': 47, 'max': 48, 'v': 23},
                {'min': 45, 'max': 46, 'v': 22},
                {'min': 42, 'max': 44, 'v': 21},
                {'min': 40, 'max': 41, 'v': 20},
                {'min': 37, 'max': 39, 'v': 19},
                {'min': 34, 'max': 36, 'v': 18},
                {'min': 32, 'max': 33, 'v': 17},
                {'min': 28, 'max': 31, 'v': 16},
                {'min': 25, 'max': 27, 'v': 15},
                {'min': 22, 'max': 24, 'v': 14},
                {'min': 18, 'max': 21, 'v': 13},
                {'min': 13, 'max': 17, 'v': 12},
                {'min': 7, 'max': 12, 'v': 11},
                {'min': 0, 'max': 6, 'v': 10},
            ],
            'Fine': [
                    {'min': 25, 'max': 72, 'v': 24},
                    {'min': 24, 'max': 24, 'v': 23},
                    {'min': 23, 'max': 23, 'v': 22},

                    {'min': 22, 'max': 22, 'v': 21},
                    {'min': 21, 'max': 21, 'v': 20},
                    {'min': 20, 'max': 20, 'v': 19},
                    {'min': 19, 'max': 19, 'v': 18},
                    {'min': 18, 'max': 18, 'v': 17},
                    {'min': 17, 'max': 17, 'v':16},
                    {'min': 16, 'max': 16, 'v': 15},
                    {'min': 15, 'max': 15, 'v': 14},
                    {'min': 14, 'max': 14, 'v':  13},
                    {'min': 12, 'max': 13, 'v': 12},
                    {'min': 11, 'max': 11, 'v': 11},
                    {'min': 10, 'max': 10, 'v': 10},
                    {'min': 8, 'max': 9, 'v': 9},
                    {'min': 7, 'max': 7, 'v': 8},
                    {'min': 5, 'max': 6, 'v': 7},
                    {'min': 3, 'max': 4, 'v': 6},
                    {'min': 0, 'max': 2, 'v': 5},
                ],
        }
        try:
            with transaction.atomic():
                # Supprimer les anciennes données pour cette tranche d'âge
                EchelleVMapping.objects.filter(
                    age_debut_annee=1,
                    age_debut_mois=0,
                    age_debut_jour=0,
                    age_fin_annee=1,
                    age_fin_mois=0,
                    age_fin_jour=30
                ).delete()

                # Charger les nouvelles données
                for sous_domaine_name, mappings in mappings_data.items():
                    try:
                        sous_domaine = SousDomain.objects.get(name=sous_domaine_name)
                        self.stdout.write(f"Traitement du sous-domaine: {sous_domaine_name}")
                        
                        for mapping in mappings:
                            EchelleVMapping.objects.create(
                                sous_domaine=sous_domaine,
                                age_debut_annee=1,
                                age_debut_mois=0,
                                age_debut_jour=0,
                                age_fin_annee=1,
                                age_fin_mois=0,
                                age_fin_jour=30,
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
                    'Toutes les données échelle-V ont été chargées avec succès pour la tranche 1:0:0-1:0:30'
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Erreur lors du chargement des données: {str(e)}'
            ))
            raise
from django.core.management.base import BaseCommand
from vineland.models import IntervaleConfianceSousDomaine
from polls.models import SousDomain

class Command(BaseCommand):
    help = 'Import des intervalles de confiance pour les sous-domaines'

    def handle(self, *args, **options):
        # Dictionnaire de mapping pour les sous-domaines
        sous_domaines = {
            # Communication
            'receptif': 'Réceptive',
            'expressif': 'Expressive',
            'ecrit': 'Écrite',
            # Vie quotidienne
            'personnel': 'Personnelle',
            'domestique': 'Domestique',
            'communaute': 'Communautaire',
            # Socialisation
            'relations_interpersonnelles': 'Relations interpersonnelles',
            'jeux_temps_libre': 'Jeu et temps libre',
            'adaptation': 'Adaptation',
            # Motricité
            'globale': 'Globale',
            'fine': 'Fine'
        }

        # Données des intervalles de confiance
        data = {
                '1': {
                    95: {
                        'receptif': 2, 'expressif': 1, 'ecrit': None, 
                        'personnel': 2, 'domestique': 3, 'communaute': 4,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': 1, 'fine': 2
                    },
                    90: {
                        'receptif': 1, 'expressif': 1, 'ecrit': None,
                        'personnel': 1, 'domestique': 2, 'communaute': 3,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': 1, 'fine': 2
                    },
                    85: {
                        'receptif': 1, 'expressif': 1, 'ecrit': None,
                        'personnel': 1, 'domestique': 2, 'communaute': 3,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': 1, 'fine': 1
                    }
                },
                '2': {
                    95: {
                        'receptif': 2, 'expressif': 1, 'ecrit': None,
                        'personnel': 1, 'domestique': 3, 'communaute': 3,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 1, 'adaptation': 2,
                        'globale': 2, 'fine': 2
                    },
                    90: {
                        'receptif': 2, 'expressif': 0, 'ecrit': None,
                        'personnel': 1, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 1, 'fine': 2
                    },
                    85: {
                        'receptif': 1, 'expressif': 0, 'ecrit': None,
                        'personnel': 1, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 1, 'fine': 2
                    }
                },
                '3': {
                    95: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': 1, 'fine': 2
                    },
                    90: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 1, 'fine': 1
                    },
                    85: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 1,
                        'personnel': 1, 'domestique': 2, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 1, 'fine': 1
                    }
                },
                '4': {
                    95: {
                        'receptif': 2, 'expressif': 2, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': 2, 'fine': 2
                    },
                    90: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': 1, 'fine': 1
                    },
                    85: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 1,
                        'personnel': 2, 'domestique': 2, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 1, 'fine': 1
                    }
                },
                '5': {
                    95: {
                        'receptif': 2, 'expressif': 2, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': 3, 'fine': 2
                    },
                    90: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 2, 'fine': 2
                    },
                    85: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 1, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 2, 'fine': 2
                    }
                },
                '6': {
                    95: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': 4, 'fine': 4
                    },
                    90: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': 4, 'fine': 3
                    },
                    85: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 1, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 3, 'fine': 3
                    }
                },
                '7-8': {
                    95: {
                        'receptif': 3, 'expressif': 1, 'ecrit': 1,
                        'personnel': 2, 'domestique': 2, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': None, 'fine': None
                    },
                    90: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 1,
                        'personnel': 2, 'domestique': 1, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': None, 'fine': None
                    },
                    85: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 1,
                        'personnel': 2, 'domestique': 1, 'communaute': 1,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': None, 'fine': None
                    }
                },
                '9-11': {
                    95: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 1, 'communaute': 3,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 3, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    90: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 1,
                        'personnel': 2, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    85: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 1,
                        'personnel': 2, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': None, 'fine': None
                    }
                },
                '12-14': {
                    95: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 3, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    90: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 2,
                        'personnel': 1, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    85: {
                        'receptif': 1, 'expressif': 1, 'ecrit': 1,
                        'personnel': 1, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': None, 'fine': None
                    }
                },
                '15-18': {
                    95: {
                        'receptif': 1, 'expressif': 3, 'ecrit': 2,
                        'personnel': 2, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 3, 'jeux_temps_libre': 3, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    90: {
                        'receptif': 1, 'expressif': 3, 'ecrit': 2,
                        'personnel': 2, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 3, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    85: {
                        'receptif': 1, 'expressif': 2, 'ecrit': 2,
                        'personnel': 1, 'domestique': 1, 'communaute': 1,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': None, 'fine': None
                    }
                },
                '19-29': {
                    95: {
                        'receptif': 3, 'expressif': 2, 'ecrit': 3,
                        'personnel': 2, 'domestique': 2, 'communaute': 3,
                        'relations_interpersonnelles': 3, 'jeux_temps_libre': 2, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    90: {
                        'receptif': 2, 'expressif': 2, 'ecrit': 3,
                        'personnel': 2, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 3, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': None, 'fine': None
                    },
                    85: {
                        'receptif': 2, 'expressif': 1, 'ecrit': 2,
                        'personnel': 2, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': None, 'fine': None
                    }
                },
                '30-49': {
                    95: {
                        'receptif': 4, 'expressif': 2, 'ecrit': 3,
                        'personnel': 3, 'domestique': 2, 'communaute': 3,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 3, 'adaptation': 2,
                        'globale': None, 'fine': None
                    },
                    90: {
                        'receptif': 3, 'expressif': 2, 'ecrit': 2,
                        'personnel': 2, 'domestique': 2, 'communaute': 3,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 3, 'adaptation': 1,
                        'globale': None, 'fine': None
                    },
                    85: {
                        'receptif': 3, 'expressif': 2, 'ecrit': 2,
                        'personnel': 2, 'domestique': 1, 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': None, 'fine': None
                    }
                },
                '50-90': {
                    95: {
                        'receptif': 2, 'expressif': 2, 'ecrit': 1,
                        'personnel': 2, 'domestique': 2, 'communaute': 3,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 2, 'adaptation': 1,
                        'globale': 1, 'fine': 2
                    },
                    90: {
                        'receptif': 2, 'expressif': 2, 'ecrit': 1,
                        'personnel': 1, 'domestique': 2, 'communaute': 2,
                        'relations_interpersonnelles': 2, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 1, 'fine': 2
                    },
                    85: {
                        'receptif': 2 , 'expressif': 2, 'ecrit': 1,
                        'personnel': 1, 'domestique': 2 , 'communaute': 2,
                        'relations_interpersonnelles': 1, 'jeux_temps_libre': 1, 'adaptation': 1,
                        'globale': 1, 'fine': 2
                    }
                }
            }

        # Supprimer les anciennes données
        IntervaleConfianceSousDomaine.objects.all().delete()

        # Créer les nouveaux intervalles
        for age, niveaux in data.items():
            for niveau, intervalles in niveaux.items():
                for sous_domaine_key, intervalle in intervalles.items():
                    if intervalle is not None:  # Ne pas créer d'entrée si l'intervalle est None
                        try:
                            sous_domaine = SousDomain.objects.get(name=sous_domaines[sous_domaine_key])
                            IntervaleConfianceSousDomaine.objects.create(
                                age=age,
                                niveau_confiance=niveau,
                                sous_domaine=sous_domaine,
                                intervalle=intervalle
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Créé intervalle pour {age} ans - {niveau}% - {sous_domaine.name}: ±{intervalle}'
                                )
                            )
                        except SousDomain.DoesNotExist:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Sous-domaine non trouvé: {sous_domaines[sous_domaine_key]}'
                                )
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Erreur lors de la création de l\'intervalle: {str(e)}'
                                )
                            )

        self.stdout.write(self.style.SUCCESS('Import terminé'))
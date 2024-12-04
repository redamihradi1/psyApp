from django.core.management.base import BaseCommand
from vineland.models import IntervaleConfianceDomaine
from polls.models import Domain

class Command(BaseCommand):
    help = 'Import des intervalles de confiance pour les domaines'

    def handle(self, *args, **options):
        # Données pour les intervalles de confiance des domaines
        data = {
            '1': {
                95: {
                    'Communication': 6,
                    'Vie quotidienne': 11,
                    'Socialisation': 8,
                    'Motricité': 7,
                    'note_composite': 5
                },
                90: {
                    'Communication': 5,
                    'Vie quotidienne': 9,
                    'Socialisation': 7,
                    'Motricité': 6,
                    'note_composite': 4
                },
                85: {
                    'Communication': 4,
                    'Vie quotidienne': 8,
                    'Socialisation': 6,
                    'Motricité': 5,
                    'note_composite': 4
                }
            },
            '2': {
                95: {
                    'Communication': 6,
                    'Vie quotidienne': 9,
                    'Socialisation': 6,
                    'Motricité': 8,
                    'note_composite': 4
                },
                90: {
                    'Communication': 5,
                    'Vie quotidienne': 7,
                    'Socialisation': 5,
                    'Motricité': 7,
                    'note_composite': 3
                },
                85: {
                    'Communication': 4,
                    'Vie quotidienne': 6,
                    'Socialisation': 4,
                    'Motricité': 6,
                    'note_composite': 3
                }
            },
            '3': {
                95: {
                    'Communication': 6,
                    'Vie quotidienne': 7,
                    'Socialisation': 6,
                    'Motricité': 7,
                    'note_composite': 4
                },
                90: {
                    'Communication': 5,
                    'Vie quotidienne': 6,
                    'Socialisation': 5,
                    'Motricité': 6,
                    'note_composite': 3
                },
                85: {
                    'Communication': 4,
                    'Vie quotidienne': 5,
                    'Socialisation': 4,
                    'Motricité': 5,
                    'note_composite': 3
                }
            },
            '4': {
                95: {
                    'Communication': 7,
                    'Vie quotidienne': 7,
                    'Socialisation': 5,
                    'Motricité': 7,
                    'note_composite': 4
                },
                90: {
                    'Communication': 6,
                    'Vie quotidienne': 6,
                    'Socialisation': 4,
                    'Motricité': 6,
                    'note_composite': 3
                },
                85: {
                    'Communication': 5,
                    'Vie quotidienne': 5,
                    'Socialisation': 4,
                    'Motricité': 5,
                    'note_composite': 3
                }
            },
            '5': {
                95: {
                    'Communication': 7,
                    'Vie quotidienne': 7,
                    'Socialisation': 6,
                    'Motricité': 12,
                    'note_composite': 5
                },
                90: {
                    'Communication': 6,
                    'Vie quotidienne': 6,
                    'Socialisation': 5,
                    'Motricité': 10,
                    'note_composite': 4
                },
                85: {
                    'Communication': 5,
                    'Vie quotidienne': 5,
                    'Socialisation': 4,
                    'Motricité': 9,
                    'note_composite': 4
                }
            },
            '6': {
                95: {
                    'Communication': 7,
                    'Vie quotidienne': 7,
                    'Socialisation': 6,
                    'Motricité': 19,
                    'note_composite': 7
                },
                90: {
                    'Communication': 6,
                    'Vie quotidienne': 6,
                    'Socialisation': 5,
                    'Motricité': 16,
                    'note_composite': 6
                },
                85: {
                    'Communication': 5,
                    'Vie quotidienne': 5,
                    'Socialisation': 4,
                    'Motricité': 14,
                    'note_composite': 5
                }
            },
            '7-8': {
                95: {
                    'Communication': 7,
                    'Vie quotidienne': 7,
                    'Socialisation': 6,
                    'Motricité': None,
                    'note_composite': 4
                },
                90: {
                    'Communication': 6,
                    'Vie quotidienne': 6,
                    'Socialisation': 5,
                    'Motricité': None,
                    'note_composite': 3
                },
                85: {
                    'Communication': 5,
                    'Vie quotidienne': 5,
                    'Socialisation': 4,
                    'Motricité': None,
                    'note_composite': 3
                }
            },
            '9-11': {
                95: {
                    'Communication': 6,
                    'Vie quotidienne': 8,
                    'Socialisation': 8,
                    'Motricité': None,
                    'note_composite': 5
                },
                90: {
                    'Communication': 5,
                    'Vie quotidienne': 7,
                    'Socialisation': 7,
                    'Motricité': None,
                    'note_composite': 4
                },
                85: {
                    'Communication': 4,
                    'Vie quotidienne': 6,
                    'Socialisation': 6,
                    'Motricité': None,
                    'note_composite': 4
                }
            },
            '12-14': {
                95: {
                    'Communication': 6,
                    'Vie quotidienne': 7,
                    'Socialisation': 8,
                    'Motricité': None,
                    'note_composite': 4
                },
                90: {
                    'Communication': 5,
                    'Vie quotidienne': 6,
                    'Socialisation': 7,
                    'Motricité': None,
                    'note_composite': 3
                },
                85: {
                    'Communication': 4,
                    'Vie quotidienne': 5,
                    'Socialisation': 6,
                    'Motricité': None,
                    'note_composite': 3
                }
            },
            '15-18': {
                95: {
                    'Communication': 10,
                    'Vie quotidienne': 7,
                    'Socialisation': 12,
                    'Motricité': None,
                    'note_composite': 8
                },
                90: {
                    'Communication': 8,
                    'Vie quotidienne': 6,
                    'Socialisation': 10,
                    'Motricité': None,
                    'note_composite': 7
                },
                85: {
                    'Communication': 7,
                    'Vie quotidienne': 5,
                    'Socialisation': 9,
                    'Motricité': None,
                    'note_composite': 6
                }
            },
            '19-29': {
                95: {
                    'Communication': 10,
                    'Vie quotidienne': 8,
                    'Socialisation': 9,
                    'Motricité': None,
                    'note_composite': 7
                },
                90: {
                    'Communication': 8,
                    'Vie quotidienne': 7,
                    'Socialisation': 8,
                    'Motricité': None,
                    'note_composite': 6
                },
                85: {
                    'Communication': 7,
                    'Vie quotidienne': 6,
                    'Socialisation': 7,
                    'Motricité': None,
                    'note_composite': 5
                }
            },
            '30-49': {
                95: {
                    'Communication': 11,
                    'Vie quotidienne': 11,
                    'Socialisation': 8,
                    'Motricité': None,
                    'note_composite': 7
                },
                90: {
                    'Communication': 9,
                    'Vie quotidienne': 9,
                    'Socialisation': 7,
                    'Motricité': None,
                    'note_composite': 6
                },
                85: {
                    'Communication': 8,
                    'Vie quotidienne': 8,
                    'Socialisation': 6,
                    'Motricité': None,
                    'note_composite': 5
                }
            },
            '50-90': {
                95: {
                    'Communication': 8,
                    'Vie quotidienne': 9,
                    'Socialisation': 6,
                    'Motricité': 8,
                    'note_composite': 6
                },
                90: {
                    'Communication': 7,
                    'Vie quotidienne': 7,
                    'Socialisation': 5,
                    'Motricité': 7,
                    'note_composite': 5
                },
                85: {
                    'Communication': 6,
                    'Vie quotidienne': 6,
                    'Socialisation': 4,
                    'Motricité': 6,
                    'note_composite': 4
                }
            }
        }

        # Supprimer les anciennes données
        IntervaleConfianceDomaine.objects.all().delete()

        # Obtenir les domaines AND FROMAUTRE = Vineland
        domains = {
                    'Communication': Domain.objects.get(name='Communication', formulaire__title ='Vineland'),
                    'Vie quotidienne': Domain.objects.get(name='Vie quotidienne', formulaire__title ='Vineland'),
                    'Socialisation': Domain.objects.get(name='Socialisation', formulaire__title ='Vineland'),
                    'Motricité': Domain.objects.get(name='Motricité', formulaire__title ='Vineland')
                }

        # Créer les nouveaux intervalles
        for age, niveaux in data.items():
            for niveau, intervalles in niveaux.items():
                for domain_name, intervalle in intervalles.items():
                    if domain_name != 'note_composite' and intervalle is not None:
                        try:
                            IntervaleConfianceDomaine.objects.create(
                                age=age,
                                niveau_confiance=niveau,
                                domain=domains[domain_name],
                                intervalle=intervalle,
                                note_composite=intervalles['note_composite']
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Créé intervalle pour {age} ans - {niveau}% - {domain_name}: ±{intervalle} (Note composite: {intervalles["note_composite"]})'
                                )
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Erreur lors de la création de l\'intervalle: {str(e)}'
                                )
                            )

        self.stdout.write(self.style.SUCCESS('Import terminé'))
from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Jeu et temps libre (8-15 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Jeu et temps libre (8-15 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Jeu et temps libre',
                domain__name='Socialisation'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=10,
                item_fin=21,
                age_debut=8,
                age_fin=15
            )

            questions = [
                {
                    'numero_item': 10,
                    'texte': "Joue avec les autres avec une surveillance minimale.",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Utilise des objets de la vie courante ou d\'autres objets pour des activités de faire-semblant (par exemple, faire semblant qu\'un cube est une voiture, une boîte est une maison, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Se protège en s\'éloignant de ceux qui détruisent des objets ou font mal (par exemple, ceux qui mordent, frappent, jettent des choses, tirent les cheveux, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Joue à des activités de faire-semblant simples avec d\'autres (par exemple, jouer à se déguiser, faire semblant d\'être un superhéros, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Recherche la compagnie des autres pour jouer ou pour être ensemble (par exemple, invite quelqu\'un à la maison, se rend chez les autres, joue avec d\'autres enfants dans une aire de jeux, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Attend son tour quand on le lui demande lorsqu\'il participe à des jeux de société ou en sport.",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Participe à des jeux de plein air improvisés, en groupe (par exemple, chat perché, corde à sauter, jeux de ballon).",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Partage ses jouets et ses affaires sans qu\'on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Suit les règles dans des jeux simples (courses de relais, loto, jeux électroniques, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Attend son tour sans qu\'on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Joue à des jeux de hasard : jeux de cartes ou jeux de société (par exemple, jeu de l\'oie, bataille, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Sort avec des amis durant la journée sous la surveillance d\'un adulte (par exemple, au centre aéré, au centre commercial, etc.).",
                    'permet_na': False
                }
            ]

            for question_data in questions:
                question, created = QuestionVineland.objects.get_or_create(
                    sous_domaine=sous_domaine,
                    numero_item=question_data['numero_item'],
                    defaults={
                        'texte': question_data['texte'],
                        'permet_na': question_data['permet_na'],
                        'note': question_data.get('note', None)
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Question {question.numero_item} créée'))

            self.stdout.write(self.style.SUCCESS('Questions Jeu et temps libre (8-15 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
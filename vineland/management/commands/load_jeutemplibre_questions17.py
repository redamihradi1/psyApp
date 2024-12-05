from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Jeu et temps libre (1-7 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Jeu et temps libre (1-7 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Jeu et temps libre',
                domain__name='Socialisation'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=9,
                age_debut=1,
                age_fin=7
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Réagit quand le parent ou la personne qui s\'occupe de lui/elle agit de façon ludique (par exemple, sourit, rit, tape des mains).",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Montre de l\'intérêt pour l\'endroit où il/elle est (par exemple, regarde autour de lui/d\'elle, se déplace, touche des objets ou des gens, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Joue à des jeux interactifs simples avec d\'autres (par exemple, « coucou », « ainsi font les petites marionnettes »).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Joue à côté d\'un autre enfant, chacun faisant une chose différente.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Choisit de jouer avec d\'autres enfants (par exemple, ne reste pas en marge d\'un groupe, n\'évite pas les autres).",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Joue de façon coopérative avec un ou plusieurs enfants moins de 5 minutes.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Joue de façon coopérative avec plusieurs enfants pendant plus de 5 minutes.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Continue à jouer avec un autre enfant sans protester lorsque le parent ou la personne qui s\'occupe de lui/d\'elle s\'en va.",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Partage ses jouets et ses affaires quand on le lui demande.",
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

            self.stdout.write(self.style.SUCCESS('Questions Jeu et temps libre (1-7 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
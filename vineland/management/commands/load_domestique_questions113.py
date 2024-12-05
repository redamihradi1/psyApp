from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour S\'occuper de son domicile (1-13 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions S\'occuper de son domicile (1-13 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Domestique',
                domain__name='Vie quotidienne'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=6,
                age_debut=1,
                age_fin=13
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Est prudent avec les objets chauds (par exemple, le four, les plaques de cuisson, le feu, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Aide à des tâches ménagères simples (par exemple, faire la poussière, ramasser les vêtements ou les jouets, nourrir les animaux, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Débarrasse son couvert (objets incassables).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Nettoie ou range l\'aire de jeu ou de travail à la fin d\'une activité (par exemple, la peinture au doigt, la construction de maquettes, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Range ses affaires à leur place (par exemple, livres, jouets, magazines, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Est prudent quand il/elle utilise des objets coupants (par exemple, ciseaux, couteaux, etc.).",
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

            self.stdout.write(self.style.SUCCESS('Questions S\'occuper de son domicile (1-13 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Comportements problématiques Section A (3+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Comportements problématiques Section A...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Section A',
                domain__name='Comportements problématiques'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=11,
                age_debut=3,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Est trop dépendant(e) (c\'est-à-dire, s\'agrippe à la personne qui s\'occupe de lui/elle, à l\'enseignant ou l\'éducateur, aux frères et sœurs).",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Évite les autres et préfère être seul(e).",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "A des difficultés d\'alimentation (par exemple, mange trop vite ou trop lentement, stocke de la nourriture, mange trop, refuse de manger, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "A des problèmes de sommeil (par exemple, somnambulisme, cauchemars fréquents, dort beaucoup moins ou beaucoup plus que les enfants de son âge).",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Refuse d\'aller à l\'école ou au travail par peur, par sentiment de rejet ou d\'isolement, etc.",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Est trop anxieux ou nerveux.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Pleure ou rit trop facilement.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "A un contact visuel pauvre (c\'est-à-dire, ne regarde pas ou ne fait pas face aux autres quand il/elle parle ou quand on lui parle).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Est triste sans raison apparente.",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Évite les interactions sociales.",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Manque d\'énergie ou d\'intérêt pour la vie.",
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

            self.stdout.write(self.style.SUCCESS('Questions Comportements problématiques Section A chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
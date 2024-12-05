from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Comportements problématiques Section B (3+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Comportements problématiques Section B...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Section B',
                domain__name='Comportements problématiques'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=10,
                age_debut=3,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Est impulsif(ve) (c\'est-à-dire, agit sans réfléchir).",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Fait des grosses crises de colère.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Désobéit volontairement et défie les représentants de l\'autorité.",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Raille, taquine ou brutalise les autres.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Est insensible aux autres ou ne les prend pas en considération.",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Ment, triche, ou vole.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Est agressif(ve) physiquement (par exemple, frappe, donne des coups de pied, mord, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Est têtu(e) ou boudeur(se).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Tient des propos embarrassants ou pose des questions gênantes en public (par exemple, « tu es gros », « c\'est quoi ce truc rouge sur ton nez ? »).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Se conduit de façon inappropriée quand les autres l\'y incitent.",
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

            self.stdout.write(self.style.SUCCESS('Questions Comportements problématiques Section B chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
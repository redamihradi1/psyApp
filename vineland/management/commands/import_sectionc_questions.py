from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Comportements problématiques Section C (3+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Comportements problématiques Section C...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Section C',
                domain__name='Comportements problématiques'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=15,
                age_debut=3,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Suce son pouce ou ses doigts.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Mouille son lit ou doit porter des couches la nuit.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Agit de façon familière avec les étrangers (par exemple, leur prend la main, les prend dans ses bras, s\'assied sur leurs genoux, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Se ronge les ongles.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "A des tics (c\'est-à-dire, des mouvements involontaires comme : clignements d\'yeux, secousses, hochement de tête, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Grince des dents le jour ou la nuit.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "A des difficultés d\'attention.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Est plus actif ou plus agité que d\'autres de même âge.",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Utilise sans autorisation du matériel de l\'école ou du travail à des fins personnelles (par exemple, téléphone, accès internet, fournitures de bureau).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Est grossier (jurons, insultes).",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Fugue (c\'est-à-dire, disparaît pendant au moins 24 heures).",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Fait l\'école buissonnière ou manque le travail sans donner de motif.",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Ignore les autres ou ne porte pas d\'attention aux personnes autour de lui/d\'elle.",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Utilise de l\'argent ou des cadeaux pour \"acheter\" de l\'affection.",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Consomme de l\'alcool ou des drogues illégales à l\'école ou au travail.",
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

            self.stdout.write(self.style.SUCCESS('Questions Comportements problématiques Section C chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
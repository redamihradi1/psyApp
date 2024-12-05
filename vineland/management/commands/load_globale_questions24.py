from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Motricité Globale (2-4 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Motricité Globale (2-4 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Globale',
                domain__name='Motricité'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=16,
                item_fin=25,
                age_debut=2,
                age_fin=4
            )

            questions = [
                {
                    'numero_item': 16,
                    'texte': "Traverse la pièce ; peut être instable et tomber occasionnellement.",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Lance une balle.",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Marche pour se déplacer ; sans se tenir à quelque chose.",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Grimpe et descend d\'une chaise d\'adulte.",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Court sans tomber ; peut être maladroit et mal coordonné.",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Monte l\'escalier, en mettant les deux pieds sur chaque marche ; peut utiliser la rampe.",
                    'permet_na': False
                },
                {
                    'numero_item': 22,
                    'texte': "Donne un coup de pied dans un ballon.",
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': "Court de façon fluide sans tomber.",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Descend l\'escalier en regardant devant lui/elle, en posant les deux pieds sur chaque marche ; peut utiliser la rampe.",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Saute en décollant les deux pieds du sol.",
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

            self.stdout.write(self.style.SUCCESS('Questions Motricité Globale (2-4 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
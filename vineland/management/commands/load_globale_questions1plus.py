from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Motricité Globale (1+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Motricité Globale (1+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Globale',
                domain__name='Motricité'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=15,
                age_debut=1,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Tient sa tête pendant au moins 15 secondes sans assistance quand le parent ou la personne qui s\'occupe de lui/elle le/la tient debout dans ses bras.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Tient assis avec un support (par exemple, dans une chaise, avec des coussins, etc.) pendant au moins une minute.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Tient assis sans support pendant au moins une minute.",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Rampe ou se déplace sur le ventre sur le sol.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Tient assis sans support pendant au moins dix minutes.",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Se met en position assise et reste assis sans support pendant au moins une minute.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Marche à quatre pattes sur au moins 1,50 mètre, sans que le ventre touche le sol.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Se met en position debout.",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Monte l\'escalier à quatre pattes ou en rampant.",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Fait au moins deux pas (sans aide).",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Se tient debout sans aide pendant 1 à 3 minutes.",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Fait rouler une balle alors qu\'il/elle est en position assise.",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Monte et descend d\'un meuble bas (par exemple, chaise, marchepied, toboggan, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Descend l\'escalier à quatre pattes ou en rampant à reculons.",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Se tient debout pendant au moins 5 minutes.",
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

            self.stdout.write(self.style.SUCCESS('Questions Motricité Globale chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
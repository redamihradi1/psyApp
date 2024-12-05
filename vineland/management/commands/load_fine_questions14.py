from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Motricité Fine (1-4 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Motricité Fine (1-4 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Fine',
                domain__name='Motricité'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=10,
                age_debut=1,
                age_fin=4
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Tend la main vers un jouet ou un objet.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Saisit de petits objets (pas plus de 6 cm de côté) ; peut utiliser les deux mains.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Passe un objet d\'une main à l\'autre.",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Presse un jouet ou un objet couineurs.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Saisit un petit objet entre le pouce et les doigts.",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Retire un objet (par exemple, un cube ou une pince à linge) d\'un récipient.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Met un objet (par exemple, un cube ou une pince à linge) dans un récipient.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Tourne une à une les pages d\'un livre en carton, en tissu ou en papier.",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Empile au moins 4 petits cubes ou autres petits objets ; la construction ne doit pas tomber.",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Ouvre les portes en tournant ou en abaissant la poignée.",
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

            self.stdout.write(self.style.SUCCESS('Questions Motricité Fine (1-4 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
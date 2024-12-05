from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Contact avec les autres (1-4 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Contact avec les autres (1-4 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Relations interpersonnelles',
                domain__name='Socialisation'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=11,
                age_debut=1,
                age_fin=4
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Regarde le visage de la personne qui s\'occupe de lui/d\'elle.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Regarde (suit des yeux) pendant au moins 5 secondes, quelqu\'un qui bouge à côté de son berceau ou de son lit.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Manifeste deux émotions ou plus (par exemple, rit, pleure, crie, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Sourit ou produit des sons à l\'approche d\'une personne familière.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Établit ou essaie d\'établir un contact avec quelqu\'un (par exemple, sourit, fait du bruit, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Lève les bras vers une personne familière quand celle-ci lui tend les bras.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Manifeste des préférences pour certaines personnes et objets (par exemple, sourit, tend la main ou se déplace vers une personne ou un objet, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Montre de l\'affection aux personnes familières (par exemple, les touche, les serre dans ses bras, les embrasse, leur fait un câlin, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Imite ou essaie d\'imiter les expressions faciales du parent ou de la personne qui s\'occupe de lui/d\'elle (par exemple, sourit, fronce les sourcils, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Se déplace pour chercher le parent ou la personne qui s\'occupe de lui/d\'elle ou une autre personne familière qui se trouve à proximité.",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Montre de l\'intérêt pour les enfants du même âge, autres que ses frères et sœurs (par exemple, les regarde, leur sourit, etc.).",
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

            self.stdout.write(self.style.SUCCESS('Questions Contact avec les autres (1-4 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
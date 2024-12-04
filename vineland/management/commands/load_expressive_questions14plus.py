from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Communication Expressive (Parler) (14+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Communication Expressive (Parler) 14+ ans...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Expressive',
                domain__name='Communication'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=40,
                item_fin=54,
                age_debut=14,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 40,
                    'texte': "Dit le jour et le mois de son anniversaire quand on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 41,
                    'texte': "Module le ton, le volume et le rythme de sa voix de manière appropriée (par exemple, ne parle pas systématiquement trop fort, trop bas, ou de façon monotone, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 42,
                    'texte': "Parle de ses expériences en détail (par exemple, raconte qui était impliqué, où l\'activité s\'est passée, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 43,
                    'texte': "Donne des consignes simples (par exemple, comment jouer à un jeu, comment fabriquer quelque chose).",
                    'note': "Entourer 2 si les consignes sont suffisamment claires pour que l\'on puisse les suivre|Entourer 1 si il/elle donne des consignes mais qu\'on n\'arrive pas à les suivre|Entourer 0 si il/elle n\'essaie jamais de donner des consignes",
                    'permet_na': True
                },
                {
                    'numero_item': 44,
                    'texte': "Utilise « entre » dans des expressions ou des phrases (par exemple, « la balle est partie entre les voitures », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 45,
                    'texte': "Donne son numéro de téléphone quand on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 46,
                    'texte': "Passe facilement d\'un sujet à un autre durant une conversation.",
                    'permet_na': False
                },
                {
                    'numero_item': 47,
                    'texte': "Reste sur un sujet durant une conversation, ne saute pas du coq à l\'âne.",
                    'permet_na': False
                },
                {
                    'numero_item': 48,
                    'texte': "Explique une idée de plusieurs façons (par exemple, « c\'est un bon livre, il est passionnant et amusant à lire »).",
                    'permet_na': False
                },
                {
                    'numero_item': 49,
                    'texte': "A des conversations qui durent 10 minutes (par exemple, raconte ses expériences, apporte des idées, partage ses sentiments, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 50,
                    'texte': "Utilise correctement des pluriels irréguliers (par exemple, chevaux, animaux, journaux, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 51,
                    'texte': "Donne son adresse complète (c\'est-à-dire, le lieu-dit, ou le nom et le numéro de la rue, de l\'appartement, la ville), avec ou sans le code postal, quand on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 52,
                    'texte': "Décrit un objectif à court-terme et ce qu\'il/elle doit faire pour l\'atteindre (par exemple, dit : « je veux avoir une bonne note à mon examen, et donc je vais travailler dur », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 53,
                    'texte': "Donne des consignes complexes aux autres (par exemple, sur la façon de se rendre en un lieu éloigné, sur une recette avec de nombreux ingrédients ou étapes, etc.).",
                    'note': "Entourer 2 si les consignes sont suffisamment claires pour que l\'on puisse les suivre|Entourer 1 si il/elle donne des consignes mais qu\'elles ne sont pas assez claires pour qu\'on arrive à les suivre|Entourer 0 si il/elle n\'essaie jamais de donner des consignes",
                    'permet_na': True
                },
                {
                    'numero_item': 54,
                    'texte': "Décrit un objectif réaliste à long terme qui peut-être atteint dans les 6 mois ou plus (par exemple, « Je veux acheter un vélo alors je vais faire du baby-sitting et rendre service pour gagner assez d\'argent pour l\'acheter »).",
                    'permet_na': False
                },
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

            self.stdout.write(self.style.SUCCESS('Questions Communication Expressive (Parler) 14+ ans chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
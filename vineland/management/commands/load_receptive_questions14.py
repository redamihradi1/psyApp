from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Communication Réceptive (1-4 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Communication Réceptive (1-4 ans)...')

        try:
            # Récupération du sous-domaine
            sous_domaine = SousDomain.objects.get(
                name='Réceptive',
                domain__name='Communication'
            )

            # Création de la plage d'âge pour les questions 1-7
            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=7,
                age_debut=1,
                age_fin=4
            )

            # Questions pour la plage 1-4 ans
            questions = [
                {
                    'numero_item': 1,
                    'texte': "Tourne les yeux et la tête en direction d'un son.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Regarde le parent ou la personne qui s'occupe de lui/elle quand il/elle entend sa voix.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Répond à l'appel de son prénom (par exemple, se tourne vers celui qui parle, sourit, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': 'Montre qu\'il/elle comprend la signification du « non », ou d\'un mot ou geste ayant la même signification (par exemple, arrête brièvement son activité).',
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': 'Montre qu\'il/elle comprend la signification du « oui », ou d\'un mot ou geste ayant la même signification (par exemple, continue son activité, sourit, etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': 'Écoute une histoire pendant au moins 5 minutes (c\'est-à-dire, reste relativement tranquille et dirige son attention vers la personne qui raconte l\'histoire).',
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': 'Désigne au moins trois parties principales du corps quand on le lui demande (par exemple, nez, bouche, mains, pieds, etc.).',
                    'permet_na': False
                },
            ]

            for question_data in questions:
                question, created = QuestionVineland.objects.get_or_create(
                    sous_domaine=sous_domaine,
                    numero_item=question_data['numero_item'],
                    defaults={
                        'texte': question_data['texte'],
                        'permet_na': question_data['permet_na']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Question {question.numero_item} créée'))

            self.stdout.write(self.style.SUCCESS('Questions Communication Réceptive (1-4 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
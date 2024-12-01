from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Communication Réceptive (5+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Communication Réceptive (5+ ans)...')

        try:
            # Récupération du sous-domaine
            sous_domaine = SousDomain.objects.get(
                name='Réceptive',
                domain__name='Communication'
            )

            # Création de la plage d'âge pour les questions 8-20
            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=8,
                item_fin=20,
                age_debut=5,
                age_fin=None  # Pas de limite d'âge supérieure
            )

            # Questions pour la plage 5+ ans
            questions = [
                {
                    'numero_item': 8,
                    'texte': "Désigne des objets familiers dans un livre ou un magazine lorsqu'ils sont nommés (par exemple, chien, voiture, tasse, clé, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Écoute les consignes.",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': 'Suit les consignes comprenant une action et un objet (par exemple, « Apporte-moi le livre », « Ferme la porte », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': 'Désigne au moins cinq parties non principales du corps quand on le lui demande (par exemple, doigts, coudes, dents, orteils, etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': 'Suit des consignes faisant intervenir deux actions ou une action et deux objets (par exemple, « assieds-toi et mange », « apporte-moi les crayons et le papier », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': 'Suit les consignes de la forme « si-alors » (par exemple, « si tu veux jouer dehors, alors range tes affaires », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': 'Écoute une histoire pendant au moins 15 minutes.',
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': 'Écoute une histoire pendant au moins 30 minutes.',
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': 'Suit des consignes en trois parties (par exemple, « brosse-toi les dents, habille-toi et fais ton lit », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': 'Suit des consignes ou des instructions entendues 5 minutes plus tôt.',
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': 'Comprend des expressions imagées (par exemple, « donne la langue au chat », « prends la porte », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': 'Écoute un cours ou une conférence pendant au moins 15 minutes.',
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': 'Écoute un cours ou une conférence pendant au moins 30 minutes.',
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

            self.stdout.write(self.style.SUCCESS('Questions Communication Réceptive (5+ ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
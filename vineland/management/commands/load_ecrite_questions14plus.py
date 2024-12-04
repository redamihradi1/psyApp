from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Communication Écrite (14+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Communication Écrite (14+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Écrite',
                domain__name='Communication'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=14,
                item_fin=25,
                age_debut=14,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 14,
                    'texte': "Lit et comprend des textes de niveau CE1 au moins.",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Classe des listes de mots par ordre alphabétique.",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Écrit de courtes notes ou messages d\'au moins 3 phrases (par exemple, des cartes postales, des messages de remerciements, des emails, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Lit et comprend des textes de niveau CM1 au moins.",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Écrit des rapports, des articles ou des rédactions d\'au moins une page ; peut utiliser un ordinateur.",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Écrit les adresses complètes du destinataire et de l\'expéditeur sur des lettres ou des colis.",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Lit et comprend des textes de niveau 6ème au moins.",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Relit ou corrige son travail écrit avant de le rendre (par exemple, vérifie la ponctuation, l\'orthographe, la grammaire, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 22,
                    'texte': "Écrit des lettres élaborées d\'au moins 10 phrases ; peut utiliser l\'ordinateur.",
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': "Lit et comprend des textes de niveau 3ème au moins.",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Lit au moins deux articles de journal par semaine (version papier ou électronique).",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Écrit des lettres officielles (par exemple, des demandes d\'information, des réclamations, des commandes, etc.) ; peut utiliser l\'ordinateur.",
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

            self.stdout.write(self.style.SUCCESS('Questions Communication Écrite (14+ ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))

from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Comportements problématiques Section D (3+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Comportements problématiques Section D...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Section D',
                domain__name='Comportements problématiques'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=14,
                age_debut=3,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Se livre à des comportements sexuels inadaptés (par exemple, s\'exhibe, se masturbe en public, fait des avances sexuelles inconvenantes, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Est obsédé(e) par des objets ou des activités (par exemple, répète constamment des mots ou des phrases, est préoccupé(e) par des objets mécaniques, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Exprime des pensées qui n\'ont aucun sens (par exemple, dit qu\'il/elle entend des voix, semble délirant(e), etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "A des habitudes ou manies bizarres (par exemple, fait des bruits répétitifs ou fait des mouvements de mains étranges, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Préfère systématiquement les objets aux personnes (par exemple, accorde plus d\'attention aux objets qu\'aux personnes, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Manifeste des comportements d\'auto-mutilation (par exemple, se cogne la tête, se frappe ou se mord, s\'arrache la peau, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Détruit délibérément ce qui appartient à l\'autre ou à lui même.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "A un discours bizarre (par exemple, parle tout seul en public, emploie des expressions ou des phrases qui n\'ont pas de sens, répète le même mot ou la même phrase en permanence, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "N\'est pas conscient de ce qui se passe autour de lui/elle (par exemple, semble dans les nuages, a le regard vide, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Se balance d\'avant en arrière de façon répétitive.",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "A une peur inhabituelle de bruits, d\'objets ou de situations ordinaires.",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Se rappelle en détail, des années après, d\'informations dont on ne se souvient pas.",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Est incapable d\'accomplir une journée normale d\'école ou de travail à cause de douleurs ou de fatigues chroniques.",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Est incapable d\'accomplir une journée normale d\'école ou de travail à cause de symptômes psychologiques.",
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

            self.stdout.write(self.style.SUCCESS('Questions Comportements problématiques Section D chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
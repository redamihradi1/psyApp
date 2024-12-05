from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Vivre dans la communauté (10-15 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Vivre dans la communauté (10-15 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Communautaire',
                domain__name='Vie quotidienne'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=12,
                item_fin=22,
                age_debut=10,
                age_fin=15
            )

            questions = [
                {
                    'numero_item': 12,
                    'texte': "Reconnaît et identifie les différentes pièces de monnaie (euros et centimes d\'euros) ; il n\'est pas nécessaire que le sujet connaisse la valeur exacte des pièces de monnaie.",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Regarde des deux côtés de la rue avant de traverser.",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Indique le jour de la semaine quand on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Montre qu\'il/elle comprend le respect de l\'intimité, pour lui/elle-même et pour les autres (par exemple, lorsqu\'il est aux toilettes ou en train de se changer).",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Montre qu\'il/elle connaît les numéros de téléphone à appeler en cas d\'urgence lorsqu\'on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Donne l\'heure à partir d\'une horloge ou d\'une montre digitale (en chiffre).",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Donne la valeur des pièces de monnaie (1, 2 euros, 10, 20, 50 centimes d\'euros).",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Reconnaît les billets de différentes valeurs (par exemple, fait référence à un billet de 5 ou 10 Euros dans la conversation).",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Respecte les feux de signalisation pour les piétons (« bonhomme vert – rouge »).",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Montre la date du jour ou une autre date sur un calendrier quand on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 22,
                    'texte': "Montre qu\'il/elle comprend que certains articles coûtent plus chers que d\'autres (par exemple, dit « j\'ai assez d\'argent pour acheter un chewing-gum mais pas pour une barre chocolatée », ou « quel crayon coûte le moins cher ? »).",
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

            self.stdout.write(self.style.SUCCESS('Questions Vivre dans la communauté (10-15 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
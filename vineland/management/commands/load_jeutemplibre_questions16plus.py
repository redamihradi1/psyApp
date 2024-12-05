from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Jeu et temps libre (16+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Jeu et temps libre (16+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Jeu et temps libre',
                domain__name='Socialisation'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=22,
                item_fin=31,
                age_debut=16,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 22,
                    'texte': "Demande la permission avant d\'utiliser un objet appartenant à un autre ou utilisé par un autre.",
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': "S\'abstient d\'entrer dans un groupe de personnes lorsque des signaux non verbaux indiquent qu\'il n\'est pas le bienvenu.",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Joue à des jeux simples qui demandent de retenir le score (par exemple, tir au but, lancé de balle au panier, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Fait preuve d\'esprit sportif (c\'est-à-dire, suit les règles, n\'est pas trop agressif, félicite l\'autre équipe ou l\'autre joueur lors de leur victoire, et ne se met pas en colère lorsqu\'il/elle perd).",
                    'permet_na': False
                },
                {
                    'numero_item': 26,
                    'texte': "Joue à plus d\'un jeu de cartes, de société ou électronique demandant de l\'habileté et de la prise de décision (par exemple, Monopoly™, tarot, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': "Sort avec des amis le soir sous la surveillance d\'adultes (par exemple, concert, cinéma, événement sportif, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': "Suit les règles dans des jeux ou des sports complexes (par exemple, football, volley, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': "Sort avec des amis durant la journée sans la surveillance d\'un adulte (par exemple, aller en ville, au parc, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 30,
                    'texte': "Planifie des activités de loisirs nécessitant d\'organiser plus de deux choses à la fois (par exemple, une sortie à la plage incluant le transport, le repas, les activités ludiques, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 31,
                    'texte': "Sort le soir avec des amis sans la surveillance d\'un adulte (par exemple, concert, cinéma, événement sportif, etc.).",
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

            self.stdout.write(self.style.SUCCESS('Questions Jeu et temps libre (16+ ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
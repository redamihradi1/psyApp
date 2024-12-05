from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Vivre dans la communauté (1-9 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Vivre dans la communauté (1-9 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Communautaire',
                domain__name='Vie quotidienne'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=11,
                age_debut=1,
                age_fin=9
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Montre qu\'il/elle comprend la fonction du téléphone (par exemple, fait semblant de téléphoner, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Parle au téléphone avec une personne familière.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Utilise la télévision ou la radio sans aide (par exemple, mettre en marche, choisir une chaîne, sélectionner un programme etc.).",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a pas de radio ou de télévision à la maison",
                    'permet_na': True
                },
                {
                    'numero_item': 4,
                    'texte': "Compte au moins 10 objets, un par un.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Montre qu\'il/elle a conscience d\'être en voiture et adopte un comportement approprié (par exemple, garde sa ceinture attachée, ne distrait pas le conducteur, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Montre qu\'il/elle comprend la fonction de l\'argent (par exemple, dit « il faut de l\'argent pour acheter quelque chose au magasin »).",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Utilise le trottoir (quand il y en a un) ou le bord de la route quand il/elle marche ou qu\'il/elle utilise un engin avec des roues (tricycle, trottinette, patins à roulettes, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Montre qu\'il/elle comprend la fonction de l\'horloge (par exemple, dit « l\'horloge sert à donner l\'heure », ou encore « à quelle heure on y va ? »).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Respecte les règles de la maison (par exemple, ne pas courir dans la maison, ne pas sauter sur les meubles, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Est capable de jouer à un jeu vidéo ou de lancer un logiciel si l\'ordinateur est allumé ; n\'a pas besoin de savoir allumer l\'ordinateur.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a pas d\'ordinateur à la maison",
                    'permet_na': True
                },
                {
                    'numero_item': 11,
                    'texte': "Va chercher la personne demandée au téléphone, ou indique à l\'interlocuteur que cette personne n\'est pas disponible.",
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

            self.stdout.write(self.style.SUCCESS('Questions Vivre dans la communauté (1-9 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
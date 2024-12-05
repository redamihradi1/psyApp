from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Contact avec les autres (16+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Contact avec les autres (16+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Relations interpersonnelles',
                domain__name='Socialisation'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=22,
                item_fin=38,
                age_debut=16,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 22,
                    'texte': "Utilise des mots pour exprimer son contentement ou son inquiétude à l\'égard des autres (par exemple, dit « bravo ! », « bravo ! tu as gagné », « est-ce que tu te sens bien ? », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': "Agit quand une autre personne a besoin d\'un coup de main (par exemple, tenir la porte ouverte, ramasser un objet tombé, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Reconnaît ce que les autres aiment et n\'aiment pas (par exemple, dit « Lucas aime le foot » ; « Marie n\'aime pas la pizza », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Montre le même degré d\'émotion que les personnes autour de lui/elle (par exemple, ne minimise ou ne dramatise pas une situation, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 26,
                    'texte': "Garde une distance appropriée entre lui/elle et les autres dans les situations sociales (par exemple, ne s\'approche pas trop près de la personne à qui il/elle parle).",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': "Parle avec d\'autres sur des sujets d\'intérêt commun (par exemple, le sport, les émissions télévisées, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': "Engage la conversation (banalités) quand il/elle rencontre des personnes qu\'il/elle connaît (par exemple, « comment vas-tu ? », « quoi de neuf ? »).",
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': "Voit ses amis régulièrement.",
                    'permet_na': False
                },
                {
                    'numero_item': 30,
                    'texte': "Évite de tenir des propos embarrassants ou méchants, ou de poser des questions impolies en public.",
                    'permet_na': False
                },
                {
                    'numero_item': 31,
                    'texte': "A des attentes raisonnables en amitié (par exemple, ne s\'attend pas à être le seul ami de quelqu\'un, ou à ce que ses amis soient toujours disponibles).",
                    'permet_na': False
                },
                {
                    'numero_item': 32,
                    'texte': "Comprend que les autres ne peuvent pas connaître ses pensées s\'il/elle ne les a pas exprimées.",
                    'permet_na': False
                },
                {
                    'numero_item': 33,
                    'texte': "Est prudent quand il/elle parle de choses personnelles.",
                    'permet_na': False
                },
                {
                    'numero_item': 34,
                    'texte': "Coopère avec d\'autres pour organiser une activité ou pour y prendre part (par exemple, une fête d\'anniversaire ou un événement sportif).",
                    'permet_na': False
                },
                {
                    'numero_item': 35,
                    'texte': "Montre qu\'il/elle comprend les allusions ou les signaux implicites dans la conversation (par exemple, comprendre que bailler peut signifier « je m\'ennuie », ou que changer rapidement de sujet de conversation peut signifier « je ne veux pas parler de ça »).",
                    'permet_na': False
                },
                {
                    'numero_item': 36,
                    'texte': "Engage une conversation en parlant de sujets qui intéressent les autres (par exemple, « alors Mathis m\'a dit que tu aimais l\'informatique ? »).",
                    'permet_na': False
                },
                {
                    'numero_item': 37,
                    'texte': "Va à des rendez-vous ou à des sorties à plusieurs.",
                    'permet_na': False
                },
                {
                    'numero_item': 38,
                    'texte': "Va à des rendez-vous amoureux.",
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

            self.stdout.write(self.style.SUCCESS('Questions Contact avec les autres (16+ ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
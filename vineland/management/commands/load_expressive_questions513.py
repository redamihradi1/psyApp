from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Communication Expressive (Parler) (5-13 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Communication Expressive (Parler) 5-13 ans...')

        try:
            # Récupération du sous-domaine
            sous_domaine = SousDomain.objects.get(
                name='Expressive',
                domain__name='Communication'
            )

            # Création de la plage d'âge pour les questions 25-39
            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=25,
                item_fin=39,
                age_debut=5,
                age_fin=13
            )

            # Questions pour la plage 5-13 ans
            questions = [
                {
                    'numero_item': 25,
                    'texte': "Donne correctement son âge quand on le lui demande.",
                    'permet_na': False
                },
                {
                    'numero_item': 26,
                    'texte': "Dit au moins 100 mots reconnaissables.",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': 'Utilise « dans », « sur », ou « sous » dans des expressions ou des phrases (par exemple, « balle va sous chaise », « pose-le sur la table », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': 'Utilise «et» dans des expressions ou des phrases (par exemple, « Maman et Papa », « je veux de la glace et du gâteau », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': 'Dit son nom et son prénom quand on le lui demande.',
                    'permet_na': False
                },
                {
                    'numero_item': 30,
                    'texte': 'Identifie et nomme la plupart des couleurs courantes (c\'est-à-dire, rouge, bleu, vert, jaune, orange, violet, marron et noir).',
                    'note': '- Entourer 2 si il/elle nomme 6 à 8 couleurs ;\n- Entourer 1 si il/elle nomme 2 à 5 couleurs ;\n- Entourer 0 si il/elle nomme 0 ou 1 couleur.',
                    'permet_na': False
                },
                {
                    'numero_item': 31,
                    'texte': 'Pose des questions commençant par « qui » ou par « pourquoi » (par exemple, « qui c\'est ? », « pourquoi je dois partir ? », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 32,
                    'texte': 'Utilise des verbes autrement qu\'à l\'infinitif (par exemple, « mange », « partent », « chante », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 33,
                    'texte': 'Utilise des indicateurs possessifs dans des expressions ou des phrases (par exemple, « c\'est son livre », « c\'est la balle de Pierre », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 34,
                    'texte': 'Utilise des pronoms dans des expressions ou des phrases ; doit utiliser le genre et la forme corrects du pronom, mais les phrases elles-mêmes peuvent ne pas être grammaticalement correctes (par exemple, « il faire ça », « ils part », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 35,
                    'texte': 'Pose des questions commençant par « quand » (par exemple, « quand est-ce qu\'on mange ? », « quand est-ce qu\'on va rentrer ? », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 36,
                    'texte': 'Utilise les temps du passé (par exemple, marchait, cuisait, etc.) ; peut utiliser des verbes irréguliers en se trompant (par exemple, « je croivais », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 37,
                    'texte': 'Utilise « derrière » ou « devant » dans des expressions ou des phrases (par exemple, « je marchais devant elle », « Pierre est derrière toi », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 38,
                    'texte': 'Prononce les mots clairement sans substitution de sons (par exemple, ne dit pas « patir » pour « partir », « sat » pour « chat », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 39,
                    'texte': 'Raconte les parties principales d\'une histoire, d\'un conte de fée ou du scénario d\'une émission de télé ; il n\'est pas nécessaire qu\'il/elle donne beaucoup de détails ni qu\'il/elle rapporte les événements dans l\'ordre exact.',
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
                        'note': question_data.get('note', None)  # Ajout de la note pour la question 30
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Question {question.numero_item} créée'))

            self.stdout.write(self.style.SUCCESS('Questions Communication Expressive (Parler) 5-13 ans chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
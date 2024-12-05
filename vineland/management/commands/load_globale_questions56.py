from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Motricité Globale (5-6 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Motricité Globale (5-6 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Globale',
                domain__name='Motricité'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=26,
                item_fin=40,
                age_debut=5,
                age_fin=6
            )

            questions = [
                {
                    'numero_item': 26,
                    'texte': "Lance une balle de n\'importe quelle taille dans une direction spécifique.",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': "Attrape un ballon de plage de taille normale à deux mains lorsqu\'il est lancé d\'une distance de 50 centimètres à 1 mètre.",
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': "Monte l\'escalier, en alternant les pieds ; peut utiliser la rampe.",
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': "Pédale sur un tricycle ou tout autre engin à trois roues sur une distance d\'au moins 2 mètres.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) si il/elle n\'a pas de tricycle ou d\'engin à trois roues.|Mais s\'il/elle en possède un et ne l\'utilise pas pour une raison quelconque, y compris le fait que la personne qui s\'occupe de lui/elle pense qu\'il/elle n\'est pas prêt, entourer 0",
                    'permet_na': True
                },
                {
                    'numero_item': 30,
                    'texte': "Saute ou sautille en avant au moins trois fois.",
                    'permet_na': False
                },
                {
                    'numero_item': 31,
                    'texte': "Saute à cloche-pied au moins une fois sans tomber ; peut se tenir à quelque chose pour garder son équilibre.",
                    'permet_na': False
                },
                {
                    'numero_item': 32,
                    'texte': "Monte et descend d\'objets hauts (par exemple, un portique, une échelle de toboggan de 1,20 mètre, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 33,
                    'texte': "Descend l\'escalier en alternant les pieds ; peut se tenir à la rampe.",
                    'permet_na': False
                },
                {
                    'numero_item': 34,
                    'texte': "Court de façon fluide, avec des changements de vitesse et de direction.",
                    'permet_na': False
                },
                {
                    'numero_item': 35,
                    'texte': "Fait du vélo avec des petites roues sur une distance d\'au moins 3 mètres.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) si il/elle n\'a pas de vélo.|Mais s\'il/elle en possède un et ne l\'utilise pas pour une raison quelconque, y compris le fait que la personne qui s\'occupe de lui/elle pense qu\'il/elle n\'est pas prêt, entourer 0",
                    'permet_na': True
                },
                {
                    'numero_item': 36,
                    'texte': "Attrape un ballon de plage de taille normale (lancé depuis au moins 1,50 mètre) à deux mains.",
                    'permet_na': False
                },
                {
                    'numero_item': 37,
                    'texte': "Saute à cloche-pied vers l\'avant avec facilité.",
                    'permet_na': False
                },
                {
                    'numero_item': 38,
                    'texte': "Sautille sur une distance d\'au moins 1,50 mètre.",
                    'permet_na': False
                },
                {
                    'numero_item': 39,
                    'texte': "Attrape une balle de la taille d\'une balle de tennis, lancée d\'au moins 3 mètres ; se déplace pour l\'attraper si nécessaire.",
                    'permet_na': False
                },
                {
                    'numero_item': 40,
                    'texte': "Fait du vélo sans petites roues et sans tomber.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) si il/elle n\'a pas de vélo.|Mais s\'il/elle en possède un et ne l\'utilise pas pour une raison quelconque, y compris le fait que la personne qui s\'occupe de lui/elle pense qu\'il/elle n\'est pas prêt, entourer 0",
                    'permet_na': True
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

            self.stdout.write(self.style.SUCCESS('Questions Motricité Globale (5-6 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
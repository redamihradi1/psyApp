from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Communication Écrite (3-13 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Communication Écrite (3-13 ans)...')

        try:
            # Récupération du sous-domaine
            sous_domaine = SousDomain.objects.get(
                name='Écrite',
                domain__name='Communication'
            )

            # Création de la plage d'âge pour les questions 1-13
            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=13,
                age_debut=3,
                age_fin=13
            )

            # Questions pour la plage 3-13 ans
            questions = [
                {
                    'numero_item': 1,
                    'texte': "Identifie une ou plusieurs lettres de l\'alphabet en tant que lettre et les distingue des chiffres.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Reconnaît son prénom en caractères d\'imprimerie.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Identifie au moins dix lettres de l\'alphabet en caractères d\'imprimerie.",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Écrit en capitale ou en cursive (en attaché) en utilisant l\'orientation correcte (par exemple, en français, de gauche à droite ; dans certaines autres langues de droite à gauche ou de bas en haut).",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Copie son prénom.",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Identifie toutes les lettres d\'imprimerie dans l\'alphabet, en majuscules et en minuscules.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Copie au moins trois mots simples à partir d\'un exemple (par exemple, chat, voir, lapin, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Écrit de mémoire son prénom et son nom.",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Lit au moins 10 mots à haute voix.",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Écrit de mémoire au moins 10 mots simples (par exemple, lit, balle, le, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Lit des histoires simples à voix haute (histoires avec des phrases de 3 à 5 mots).",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Écrit des phrases simples de trois à quatre mots ; peut faire des petites fautes d\'orthographe ou de grammaire.",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Écrit de mémoire plus de 20 mots ; peut faire des fautes d\'orthographe.",
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
                        'note': question_data.get('note', None)
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Question {question.numero_item} créée'))

            self.stdout.write(self.style.SUCCESS('Questions Communication Écrite (3-13 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
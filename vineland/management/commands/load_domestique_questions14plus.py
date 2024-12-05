from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour S\'occuper de son domicile (14+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions S\'occuper de son domicile (14+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Domestique',
                domain__name='Vie quotidienne'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=7,
                item_fin=24,
                age_debut=14,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 7,
                    'texte': "Débarrasse son couvert (y compris les objets fragiles).",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Aide à la préparation de plats nécessitant mélange et cuisson (par exemple, purée en flocons, pâte à gâteau etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Utilise des appareils ménagers simples (par exemple, un grille-pain, un décapsuleur, un tire-bouchon, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Utilise le micro-ondes pour réchauffer ou cuire des aliments (y compris le choix du programme, de la durée et la puissance).",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a pas de micro-ondes à la maison",
                    'permet_na': True
                },
                {
                    'numero_item': 11,
                    'texte': "Range les vêtements propres à leur place (par exemple, dans des tiroirs ou un placard, sur des cintres, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Utilise des outils (par exemple, un marteau pour planter des clous, un tournevis pour visser et dévisser des vis, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Lave la vaisselle à la main ou remplit et utilise un lave-vaisselle.",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Passe le balai, la serpillière ou l\'aspirateur soigneusement.",
                    'note': "Entourer 2 si le ménage est suffisamment bien fait et qu\'il n\'est pas utile de repasser derrière|Entourer 1 si la tâche n\'est pas accomplie totalement|Entourer 0 si la tâche n\'est jamais accomplie ou s\'il faut systématiquement repasser derrière",
                    'permet_na': True
                },
                {
                    'numero_item': 15,
                    'texte': "Débarrasse la table complètement (par exemple, vide et empile la vaisselle, jette ce qui va à la poubelle, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Utilise correctement des produits d\'entretien (par exemple, lessive, cire pour les meubles, produit à vitres, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Prépare un repas simple nécessitant de la cuisson mais sans préparation particulière (par exemple, du riz, de la soupe en sachet, des légumes surgelés, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Nettoie une ou plusieurs pièces (en plus de sa propre chambre).",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Utilise un couteau aiguisé pour préparer le repas.",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Utilise la cuisinière ou le four pour chauffer, cuire ou cuisiner (par exemple, allume les plaques ou le four, sélectionne la température, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Prépare un plat nécessitant de mesurer des quantités, de mélanger et de cuire plusieurs ingrédients.",
                    'permet_na': False
                },
                {
                    'numero_item': 22,
                    'texte': "Lave le linge quand c\'est nécessaire.",
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': "Effectue des tâches d\'entretien courant quand c\'est nécessaire (par exemple, changer les ampoules, changer le sac de l\'aspirateur, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Prévoit et prépare le repas principal de la journée.",
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

            self.stdout.write(self.style.SUCCESS('Questions S\'occuper de son domicile (14+ ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
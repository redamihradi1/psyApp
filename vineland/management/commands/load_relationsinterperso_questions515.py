from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Contact avec les autres (5-15 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Contact avec les autres (5-15 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Relations interpersonnelles',
                domain__name='Socialisation'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=12,
                item_fin=21,
                age_debut=5,
                age_fin=15
            )

            questions = [
                {
                    'numero_item': 12,
                    'texte': "Imite des mouvements simples (par exemple, tape dans ses mains, fait au revoir, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Manifeste par des actions son contentement ou son inquiétude à l\'égard des autres (par exemple, serre dans ses bras, tapote le bras, tient la main, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Cherche à faire plaisir aux autres (par exemple, partage une friandise ou un jouet, essaie d\'aider même s\'il/elle n\'y arrive pas, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "A des comportements de recherche d\'amitié avec d\'autres jeunes de même âge (par exemple, dit « tu veux jouer ? » ou prend un enfant par la main).",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Imite des actions relativement complexes pendant que quelqu\'un d\'autre les réalise (par exemple, se raser, mettre du maquillage, se limer les ongles, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Répond quand des adultes familiers engagent la conversation (par exemple, si on lui demande « comment vas-tu ? », répond « je vais très bien » ; si on lui dit « tu es bien gentil! », répond « merci », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Répète des phrases entendues précédemment de la part d\'un adulte (par exemple, « chéri(e), je suis rentré(e) » ; « pas de dessert avant d\'avoir fini ton assiette » ; etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Utilise des mots pour exprimer ses émotions (par exemple, « je suis content(e) », ou « j\'ai peur »).",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "A un meilleur ami ou des préférences pour certains amis plutôt que d\'autres (garçons ou filles).",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Imite des actions relativement complexes plusieurs heures après avoir vu quelqu\'un les exécuter (par exemple, se raser, mettre du maquillage, se limer les ongles, etc.).",
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

            self.stdout.write(self.style.SUCCESS('Questions Contact avec les autres (5-15 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
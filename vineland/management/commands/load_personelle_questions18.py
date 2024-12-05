from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Prendre soin de soi (1-8 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Prendre soin de soi (1-8 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Personnelle',
                domain__name='Vie quotidienne'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=22,
                age_debut=1,
                age_fin=8
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Ouvre la bouche quand on lui présente de la nourriture.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Mange des aliments solides (par exemple, des légumes cuits, de la viande en morceaux, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Suce ou mâche de la nourriture que l\'on peut manger avec les doigts (par exemple, biscuits, chips, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Boit dans un verre ou une tasse ; peut en renverser.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Fait comprendre que ses couches sont souillées ou mouillées (par exemple, en montrant, vocalisant, ou en tirant sur sa couche).",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Mange seul avec une cuillère ; peut en renverser.",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "Boit avec une paille.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Enlève un vêtement qui s\'ouvre par devant (par exemple, un manteau ou un gilet) ; n\'a pas besoin de savoir déboutonner ou défaire la fermeture éclair.",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Enfile des vêtements à ceinture élastique qui se remontent (par exemple, pantalon de jogging, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Mange seul avec une fourchette ; peut en renverser.",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Boit dans un verre ou une tasse sans en renverser.",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Mange seul avec une cuillère sans en renverser.",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Urine aux toilettes ou sur le pot.",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Met un vêtement qui s\'ouvre par devant (par exemple, un manteau ou un gilet) ; n\'a pas besoin de savoir boutonner ou monter la fermeture éclair.",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Demande à aller aux toilettes.",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Défèque aux toilettes ou sur le pot.",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Est propre le jour.",
                    'note': "Entourer 2 si il/elle utilise les toilettes sans aide et sans accidents|Entourer 1 si il/elle a besoin d\'aide par exemple, pour s\'essuyer ou s\'il y a quelques accidents|Entourer 0 si il/elle toujours besoin d\'aide ou a de fréquents accidents",
                    'permet_na': True
                },
                {
                    'numero_item': 18,
                    'texte': "Remonte une fermeture éclair déjà attachée en bas (par exemple, sur un pantalon ou un sac à dos, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Se mouche ou s\'essuie le nez en utilisant un mouchoir.",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Est propre la nuit.",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Met ses chaussures au bon pied ; n\'a pas besoin de faire ses lacets.",
                    'permet_na': False
                },
                {
                    'numero_item': 22,
                    'texte': "Ferme des boutons-pression.",
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

            self.stdout.write(self.style.SUCCESS('Questions Prendre soin de soi (1-8 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
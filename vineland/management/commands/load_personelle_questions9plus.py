from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Prendre soin de soi (9+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Prendre soin de soi (9+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Personnelle',
                domain__name='Vie quotidienne'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=23,
                item_fin=41,
                age_debut=9,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 23,
                    'texte': "Tient sa cuillère, sa fourchette et son couteau correctement.",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Se lave (en utilisant de l\'eau et du savon) et se sèche le visage.",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Se brosse les dents.",
                    'note': "Entourer 2 si il/elle se brosse les dents sans aide, y compris pour mettre le dentifrice, sans avoir besoin qu\'on le lui rappelle|Entourer 1 si il/elle a besoin d\'aide pour le brossage ou pour mettre le dentifrice, ou si il/elle a besoin de fréquents rappels|Entourer 0 si il/elle ne se brosse jamais les dents sans aide ou sans qu\'on le lui rappelle",
                    'permet_na': True
                },
                {
                    'numero_item': 26,
                    'texte': "Boutonne de gros boutons de devant dans les bonnes boutonnières.",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': "Se couvre la bouche et le nez quand il/elle tousse ou éternue.",
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': "Boutonne les petits boutons de devant dans les bonnes boutonnières.",
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': "Attache et remonte une fermeture éclair qui n\'est pas fixée en bas (par exemple, sur un gilet ou un sweat-shirt, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 30,
                    'texte': "Ouvre les robinets et ajuste la température en ajoutant de l\'eau froide ou chaude.",
                    'permet_na': False
                },
                {
                    'numero_item': 31,
                    'texte': "Porte des vêtements appropriés quand il fait humide ou froid (par exemple, un imperméable, des bottes, un sweat-shirt, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 32,
                    'texte': "Prend un bain ou une douche et se sèche de manière autonome.",
                    'note': "Entourer 2 si il/elle le fait sans aide (y compris ouvrir et fermer les robinets)|Entourer 1 si il/elle a besoin d\'aide pour se laver ou se sécher, pour ouvrir ou fermer les robinets|Entourer 0 si il/elle ne prend jamais de bain ni de douche sans aide ou sans qu\'on le lui rappelle",
                    'permet_na': True
                },
                {
                    'numero_item': 33,
                    'texte': "Trouve et utilise les toilettes publiques adaptées à son sexe (hommes/femmes).",
                    'permet_na': False
                },
                {
                    'numero_item': 34,
                    'texte': "Se lave et se sèche les cheveux (avec une serviette ou un sèche-cheveux).",
                    'permet_na': False
                },
                {
                    'numero_item': 35,
                    'texte': "Prend soin de ses blessures superficielles (par exemple, nettoie la plaie, met un pansement, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 36,
                    'texte': "Prend des médicaments en suivant les indications sur la notice.",
                    'permet_na': False
                },
                {
                    'numero_item': 37,
                    'texte': "Utilise le thermomètre pour prendre sa température ou celle de quelqu\'un d\'autre.",
                    'permet_na': False
                },
                {
                    'numero_item': 38,
                    'texte': "Demande de l\'aide médicale en cas d\'urgence (par exemple, reconnaît les symptômes de maladie ou de blessure sérieuse, comme des difficultés respiratoires, des douleurs dans la poitrine, un saignement incontrôlé, etc.).",
                    'note': "Il est possible d\'entourer NA (Non Applicable) si il/elle n\'a jamais été confronté(e) à une urgence médicale",
                    'permet_na': True
                },
                {
                    'numero_item': 39,
                    'texte': "Suit des prescriptions médicales pour des soins de santé (régime alimentaire spécial, traitement médical).",
                    'note': "Il est possible d\'entourer NA (Non Applicable) si il/elle n\'a pas de problèmes de santé particuliers",
                    'permet_na': True
                },
                {
                    'numero_item': 40,
                    'texte': "Gère sa pharmacie personnelle (médicaments prescrits et non prescrits) et se réapprovisionne si nécessaire.",
                    'permet_na': False
                },
                {
                    'numero_item': 41,
                    'texte': "Prend rendez-vous pour des examens de routine, médicaux et dentaires.",
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

            self.stdout.write(self.style.SUCCESS('Questions Prendre soin de soi (9+ ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Communication Expressive (Parler) (1-4 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Communication Expressive (Parler)...')

        try:
            # Récupération du sous-domaine
            sous_domaine = SousDomain.objects.get(
                name='Expressive',
                domain__name='Communication'
            )

            # Création de la plage d'âge pour les questions 1-24
            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=24,
                age_debut=1,
                age_fin=4
            )

            # Questions pour la plage 1-4 ans
            questions = [
                {
                    'numero_item': 1,
                    'texte': "Pleure ou s'agite quand il/elle a faim ou qu'il/elle est mouillé(e).",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Sourit quand on lui sourit.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Fait des petits bruits de plaisir (par exemple, gazouille, rit, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': 'Fait des bruits non-verbaux de bébé (par exemple, babille – « areuh »).',
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': 'Fait des bruits ou des gestes (par exemple, agite les bras) pour attirer l\'attention de son parent ou de la personne qui s\'occupe de lui/d\'elle.',
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': 'Fait des bruits ou des gestes (par exemple, hoche la tête) si il/elle veut qu\'une activité continue ou s\'arrête.',
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': 'Fait au revoir de la main quand une autre personne le fait ou quand le parent ou la personne qui s\'occupe de lui/d\'elle lui dit de le faire.',
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': 'Dit « Pa-pa », « Ma-ma », ou un autre nom pour désigner le parent ou la personne qui s\'occupe de lui/elle (y compris le prénom ou le surnom de la personne en question).',
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': 'Montre du doigt un objet qu\'il/elle veut et qui est hors de portée.',
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': 'Montre du doigt ou fait un geste pour indiquer sa préférence lorsqu\'on lui propose un choix (par exemple, « tu veux ça ou ça ? », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': 'Répète ou essaie de répéter des mots courants immédiatement après les avoir entendus (par exemple, « balle», «voiture», on y «va», etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': 'Nomme au moins trois objets (par exemple, biberon, chien, jouet favori, etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': 'Formule des demandes en un mot (par exemple, porter, encore, dehors, etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': 'Utilise les prénoms ou les surnoms de ses frères, sœurs ou amis, ou dit leurs noms quand on le lui demande.',
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': 'Répond ou essaie de répondre avec des mots quand on lui pose une question.',
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': 'Nomme au moins 10 objets.',
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': 'Dit son prénom ou son surnom (par exemple, Julie, Petite Sœur, etc.) quand on le lui demande.',
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': 'Fait des phrases avec un sujet et un verbe (par exemple, « papa parti », « aller maison », etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': 'Pose des questions en changeant l\'intonation du mot ou de l\'expression (par exemple, « à moi ? », « moi partir ? ») ; la grammaire n\'est pas importante.',
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': 'Dit au moins 50 mots reconnaissables.',
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': 'Utilise des mots simples pour décrire des choses (par exemple, sale, joli, grand, fort, etc.).',
                    'permet_na': False
                },
                {
                    'numero_item': 22,
                    'texte': 'Pose des questions commençant par « c\'est quoi », « où », « pourquoi », « c\'est qui », ou « qu\'est-ce que c\'est ? », (par exemple, « qu\'est-ce que c\'est ? », ou « chien ? »).',
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': 'Utilise des négations dans les phrases (par exemple, « moi pas partir », « je ne le boirai pas », etc.) ; la grammaire n\'est pas importante.',
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': 'Raconte ce qui lui est arrivé dans des phrases simples (par exemple, « moi et Pierre jouer » ; « Paul m\'a lu un livre », etc.).',
                    'permet_na': False
                },
            ]

            for question_data in questions:
                question, created = QuestionVineland.objects.get_or_create(
                    sous_domaine=sous_domaine,
                    numero_item=question_data['numero_item'],
                    defaults={
                        'texte': question_data['texte'],
                        'permet_na': question_data['permet_na']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Question {question.numero_item} créée'))

            self.stdout.write(self.style.SUCCESS('Questions Communication Expressive (Parler) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
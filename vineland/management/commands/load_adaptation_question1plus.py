from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Adaptation de la socialisation (1+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Adaptation de la socialisation (1+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Adaptation',
                domain__name='Socialisation'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=1,
                item_fin=30,
                age_debut=1,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 1,
                    'texte': "Passe facilement d\'une activité à l\'autre à la maison.",
                    'permet_na': False
                },
                {
                    'numero_item': 2,
                    'texte': "Dit « merci » quand on lui donne quelque chose.",
                    'permet_na': False
                },
                {
                    'numero_item': 3,
                    'texte': "Change de comportement selon qu\'il/elle connaît plus ou moins bien la personne (par exemple, agit différemment avec un membre de la famille et avec un étranger, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 4,
                    'texte': "Mange la bouche fermée.",
                    'permet_na': False
                },
                {
                    'numero_item': 5,
                    'texte': "Dit « s\'il te plaît » quand il/elle demande quelque chose.",
                    'permet_na': False
                },
                {
                    'numero_item': 6,
                    'texte': "Termine les conversations de manière appropriée (par exemple, dit « au revoir », « à bientôt », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 7,
                    'texte': "S\'essuie la bouche ou les mains pendant et/ou après le repas.",
                    'permet_na': False
                },
                {
                    'numero_item': 8,
                    'texte': "Réagit de manière appropriée à des changements modérés de ses habitudes (par exemple, s\'abstient de se plaindre, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 9,
                    'texte': "Dit « pardon » pour des fautes involontaires (par exemple, bousculer quelqu\'un).",
                    'permet_na': False
                },
                {
                    'numero_item': 10,
                    'texte': "Évite de narguer, taquiner ou maltraiter.",
                    'permet_na': False
                },
                {
                    'numero_item': 11,
                    'texte': "Se comporte de façon appropriée quand on lui présente des étrangers (par exemple, salue de la tête, sourit, serre la main, dit bonjour, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Modifie le volume de sa voix en fonction de l\'endroit ou de la situation (par exemple, à la bibliothèque, au cinéma, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Présente des excuses quand il/elle a fait de la peine à quelqu\'un.",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "S\'abstient de parler la bouche pleine.",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Parle avec les autres sans interrompre ou être impoli.",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Accepte des suggestions ou des solutions utiles de la part des autres.",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Contrôle sa colère ou sa peine en cas de changement de programme pour une raison indépendante de sa volonté (par exemple, en cas de mauvais temps ou de panne de voiture, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Garde des secrets ou des confidences pendant plus d\'un jour.",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Dit qu\'il/elle est désolé(e) quand il/elle commet involontairement une faute ou une erreur de jugement (par exemple, si sans le faire exprès, il/elle a laissé de côté un camarade au cours d\'un jeu).",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Montre qu\'il/elle comprend que le fait de se taquiner entre amis ou au sein de la famille peut être une forme d\'humour ou une marque d\'affection.",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Informe ses parents ou la personne qui s\'occupe de lui/d\'elle de son emploi du temps (par exemple, l\'heure de départ ou de retour, l\'endroit où il/elle se rend, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 22,
                    'texte': "Choisit d\'éviter les activités dangereuses ou risquées (par exemple, sauter de très haut, prendre un auto-stoppeur, conduire dangereusement, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': "Contrôle sa colère ou sa peine quand il/elle n\'obtient pas ce qu\'il/elle veut (par exemple, s\'il/elle n\'a pas la permission de regarder la télévision ou d\'assister à une fête, ou si une suggestion qu\'il/elle fait est rejetée par un ami ou la personne qui s\'occupe de lui/elle).",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Est fidèle à ses engagements (par exemple, s\'il/si elle promet de rencontrer quelqu\'un, le rencontre, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Se tient à l\'écart ou met un terme à des relations ou des situations qui peuvent lui nuire ou être dangereuses (par exemple, moqueries, harcèlement moral, abus sexuel, escroquerie, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 26,
                    'texte': "Contrôle sa colère ou sa peine face à une critique constructive (par exemple, correction d\'un comportement inadapté, discussion d\'une note obtenue à un test, évaluation des performances, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': "Garde des secrets ou des confidences aussi longtemps que nécessaire.",
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': "Réfléchit aux conséquences de ses actions avant de prendre des décisions (par exemple, évite d\'agir de façon impulsive, prend en compte des informations importantes, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': "A conscience du danger potentiel et se montre prudent dans les situations sociales « à risque » (par exemple, les fêtes alcoolisées, les forums Internet, les petites annonces, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 30,
                    'texte': "Se montre respectueux de ses collègues de travail (par exemple, ne distrait pas et n\'interrompt pas les autres lorsqu\'ils travaillent, est à l\'heure pour les réunions, etc.).",
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

            self.stdout.write(self.style.SUCCESS('Questions Adaptation de la socialisation chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
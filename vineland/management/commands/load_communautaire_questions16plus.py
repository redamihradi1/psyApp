from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Vivre dans la communauté (16+ ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Vivre dans la communauté (16+ ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Communautaire',
                domain__name='Vie quotidienne'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=23,
                item_fin=44,
                age_debut=16,
                age_fin=None
            )

            questions = [
                {
                    'numero_item': 23,
                    'texte': "Donne l\'heure par demi-heure sur une montre ou une horloge à aiguilles (par exemple, « il est 13h30 », « il est 14h00 », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Utilise le téléphone pour appeler les autres (en utilisant un fixe ou un portable).",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Commande un menu complet dans un fast-food.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) si la personne n\'a jamais mangé au fast-food",
                    'permet_na': True
                },
                {
                    'numero_item': 26,
                    'texte': "Transporte ou range son argent de façon sûre (dans un porte-monnaie, un portefeuille, une sacoche, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': "Donne l\'heure par tranches de 5 minutes sur une montre ou une horloge à aiguilles (par exemple, « il est 11h05 », « il est 13h10 », etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': "Respecte l\'horaire du retour à la maison fixé par ses parents ou la personne qui s\'occupe de lui/d\'elle.",
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': "Regarde ou écoute des programmes pour s\'informer (par exemple, les prévisions météo, les nouvelles, les documentaires, etc.).",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a pas de radio ou de télévision à la maison",
                    'permet_na': True
                },
                {
                    'numero_item': 30,
                    'texte': "Compte la monnaie qu\'on lui rend lors d\'un achat.",
                    'permet_na': False
                },
                {
                    'numero_item': 31,
                    'texte': "Montre des connaissances en informatique pour exécuter des tâches complexes (par exemple, faire du traitement de texte, accéder à Internet, installer un logiciel, etc.).",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a pas d\'ordinateur à la maison",
                    'permet_na': True
                },
                {
                    'numero_item': 32,
                    'texte': "Évalue le prix et la qualité des produits avant de les acheter.",
                    'permet_na': False
                },
                {
                    'numero_item': 33,
                    'texte': "Respecte les horaires des pauses (par exemple, les pauses-café ou déjeuner, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 34,
                    'texte': "Fait des trajets d\'au moins 10 à 15 kilomètres pour se rendre dans un endroit familier (à vélo, en empruntant les transports en commun, ou en conduisant).",
                    'permet_na': False
                },
                {
                    'numero_item': 35,
                    'texte': "Montre qu\'il/elle comprend qu\'il/elle peut faire une réclamation ou rapporter des problèmes légitimes quand il/elle n\'est pas satisfait(e) d\'un service ou d\'une situation.",
                    'permet_na': False
                },
                {
                    'numero_item': 36,
                    'texte': "Avertit l\'école ou son responsable lorsqu\'il/elle va être en retard ou absent.",
                    'permet_na': False
                },
                {
                    'numero_item': 37,
                    'texte': "Utilise un compte courant ou un compte d\'épargne de façon responsable (par exemple, en gardant un peu d\'argent sur son compte, ou en vérifiant que les comptes sont équilibrés).",
                    'permet_na': False
                },
                {
                    'numero_item': 38,
                    'texte': "Fait des trajets d\'au moins 10 à 15 kilomètres pour se rendre dans un endroit non familier (à vélo, en empruntant les transports en commun, ou en conduisant).",
                    'permet_na': False
                },
                {
                    'numero_item': 39,
                    'texte': "Gagne de l\'argent en travaillant à temps partiel (au moins 10 heures par semaine) pendant une année.",
                    'note': "Ne pas entourer 1",
                    'permet_na': False
                },
                {
                    'numero_item': 40,
                    'texte': "Essaie d\'améliorer ses performances au travail après avoir reçu des critiques constructives de son responsable.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) si la personne n\'a pas encore eu l\'occasion de travailler",
                    'permet_na': True
                },
                {
                    'numero_item': 41,
                    'texte': "Gère son argent (par exemple, paie lui-même la plupart de ses dépenses, utilise des chèques ou des virements bancaires pour ses achats, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 42,
                    'texte': "A eu un travail à temps plein durant une année.",
                    'note': "Ne pas entourer 1",
                    'permet_na': False
                },
                {
                    'numero_item': 43,
                    'texte': "Fait un budget pour les dépenses mensuelles (le loyer, les dépenses courantes, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 44,
                    'texte': "Fait une demande de carte de crédit et l\'utilise de manière responsable (n\'excède pas la limite de crédit, respecte les délais de paiement, etc.).",
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

            self.stdout.write(self.style.SUCCESS('Questions Vivre dans la communauté (16+ ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
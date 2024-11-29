# from ..models import StudentScore, Response, ScoreParametrage, AgeTranche, AgeDeveloppeParametrage

from ..models import StudentScore, Response, ScoreParametrage, AgeTranche, AgeDeveloppeParametrage ,NoteStandardPercentile
from django.db.models import Sum

class ScoreCalculator:
    NIVEAU_DEVELOP = [
        {"min": 0, "max": 25, "niveau": "Sévère"},
        {"min": 26, "max": 74, "niveau": "Modéré"},
        {"min": 75, "max": 84, "niveau": "Léger"},
        {"min": 85, "max": 1000, "niveau": "Approprié"},
    ]

    DOMAINS = {
        "domaine1": "Communication",
        "domaine2": "Motricité",
        "domaine3": "Comportements inadaptés",
    }

    def __init__(self, student, questionnaire):
        self.student = student
        self.questionnaire = questionnaire
        self.age_in_months = self.calculate_age_in_months()
        self.tranche = self.get_age_tranche()
        self.resultat_final = []
        self.deuxieme_tableau = []
        self.init_resultat_final()
        self.init_deuxieme_tableau()
        
    def init_resultat_final(self):
        self.resultat_final = [
            {'domaine': self.DOMAINS["domaine1"], 'sousdomaine': 'CVP', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Cognition Verbale/Préverbale (CVP)'},
            {'domaine': self.DOMAINS["domaine1"], 'sousdomaine': 'LE', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Langage Expressif (LE)'},
            {'domaine': self.DOMAINS["domaine1"], 'sousdomaine': 'LR', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Langage Réceptif (LR)'},
            {'domaine': self.DOMAINS["domaine2"], 'sousdomaine': 'MF', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Motricité Fine (MF)'},
            {'domaine': self.DOMAINS["domaine2"], 'sousdomaine': 'MG', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Motricité Globale (MG)'},
            {'domaine': self.DOMAINS["domaine2"], 'sousdomaine': 'IOM', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Imitation Oculo-Motrice (IOM)'},
            {'domaine': self.DOMAINS["domaine3"], 'sousdomaine': 'EA', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Expression Affective (EA)'},
            {'domaine': self.DOMAINS["domaine3"], 'sousdomaine': 'RS', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Réciprocité Sociale (RS)'},
            {'domaine': self.DOMAINS["domaine3"], 'sousdomaine': 'CMC', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Comportements Moteurs Caractéristiques (CMC)'},
            {'domaine': self.DOMAINS["domaine3"], 'sousdomaine': 'CVC', 'total': 0, 'age_developpe': '', 'ns': '', 'percentile': '', 'niveau': '', 'label': 'Comportements Verbaux Caractéristiques (CVC)'}
        ]
    
    def init_deuxieme_tableau(self):
        """Initialisation du deuxième tableau avec tous les sous-domaines"""
        self.deuxieme_tableau = [
            {
                'domaine': self.DOMAINS["domaine1"], 
                'CVP': 0, 'LE': 0, 'LR': 0, 'MF': 0, 'MG': 0, 'IOM': 0, 
                'EA': 0, 'RS': 0, 'CMC': 0, 'CVC': 0,
                'somme_ns': 0, 'percentile': '', 'niveau': '', 'age_developpe': ''
            },
            {
                'domaine': self.DOMAINS["domaine2"], 
                'CVP': 0, 'LE': 0, 'LR': 0, 'MF': 0, 'MG': 0, 'IOM': 0, 
                'EA': 0, 'RS': 0, 'CMC': 0, 'CVC': 0,
                'somme_ns': 0, 'percentile': '', 'niveau': '', 'age_developpe': ''
            },
            {
                'domaine': self.DOMAINS["domaine3"], 
                'CVP': 0, 'LE': 0, 'LR': 0, 'MF': 0, 'MG': 0, 'IOM': 0, 
                'EA': 0, 'RS': 0, 'CMC': 0, 'CVC': 0,
                'somme_ns': 0, 'percentile': '', 'niveau': '', 'age_developpe': ''
            }
        ]

    def calculate_age_in_months(self):
        if not self.student.date_of_birth:
            return None
        today = self.questionnaire.created_at.date()
        birth_date = self.student.date_of_birth
        months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
        return months

    def get_age_tranche(self):
        return AgeTranche.objects.get(
            min_months__lte=self.age_in_months,
            max_months__gte=self.age_in_months
        )

    def calculate(self):
        # Récupérer les réponses et calculer les totaux
        responses = Response.objects.filter(
            questionnaire=self.questionnaire
        ).exclude(
            question__sous_domain__name='Autre'
        ).select_related('question', 'question__sous_domain')
        
        # Grouper les réponses par sous-domaine
        response_totals = {}
        for response in responses:
            sous_domain = response.question.sous_domain.name
            if sous_domain not in response_totals:
                response_totals[sous_domain] = 0
            response_totals[sous_domain] += response.answer
        
        # Mettre à jour les totaux dans resultat_final
        for result in self.resultat_final:
            sous_domain = result['sousdomaine']
            if sous_domain in response_totals:
                result['total'] = response_totals[sous_domain]
                
        # Calculer les scores selon la tranche d'âge
        self.calculate_scores_for_tranche()
        
        # Calculer le deuxième tableau
        self.calculate_deuxieme_tableau()
        
        return self.resultat_final, self.deuxieme_tableau

    def calculate_scores_for_tranche(self):
        print("Starting calculate_scores_for_tranche")
        parametrage = ScoreParametrage.objects.filter(tranche=self.tranche)
        
        for result in self.resultat_final:
            matching_params = parametrage.filter(
                sous_domain=result['sousdomaine'],
                score_brut=result['total']
            ).first()
            
            if matching_params:
                result['ns'] = matching_params.ns
                result['percentile'] = matching_params.percentile
                result['niveau'] = self.get_niveau(matching_params.percentile)
                
                # Get age développé
                age_param = AgeDeveloppeParametrage.objects.filter(
                    sous_domain=result['sousdomaine'],
                    score_brut=result['total']
                ).first()
                
                if age_param:
                    result['age_developpe'] = age_param.age_developpe

    def get_percentile_from_db(self, domaine, somme_ns):
        print(f"Getting percentile for domain {domaine} with NS sum {somme_ns}")
        
        try:
            # Chercher d'abord une correspondance exacte
            #make the somme_ns int 
            somme_ns = int(somme_ns)
            percentile_obj = NoteStandardPercentile.objects.filter(
                domain=domaine,
                somme_score_standard=str(somme_ns)
            ).first()
            
            if percentile_obj:
                return percentile_obj.rang_percentile
                
            # Si pas de correspondance exacte, chercher les seuils avec '>'
            seuils = NoteStandardPercentile.objects.filter(
                domain=domaine,
                somme_score_standard__startswith='>'
            )
            
            for seuil in seuils:
                # Extraire le nombre après le '>'
                valeur_seuil = int(seuil.somme_score_standard.replace('>', '').strip())
                if somme_ns > valeur_seuil:
                    return seuil.rang_percentile
                    
            return None
            
        except Exception as e:
            print(f"Error in get_percentile_from_db: {str(e)}")
            return None
        

    # def calculate_deuxieme_tableau(self):
    #     print("Starting calculate_deuxieme_tableau")
        
    #     # Seuils pour les percentiles >99 par domaine
    #     SEUILS_PERCENTILE = {
    #         "Communication": 49,
    #         "Motricité": 42,
    #         "Comportements inadaptés": 61
    #     }

    #     # Mapping des sous-domaines par domaine
    #     SOUS_DOMAINES = {
    #         "Communication": ['CVP', 'LE', 'LR'],
    #         "Motricité": ['MF', 'MG', 'IOM'],
    #         "Comportements inadaptés": ['EA', 'RS', 'CMC', 'CVC']
    #     }

    #     # Dictionnaire pour stocker les sommes d'âges par domaine
    #     ages_par_domaine = {
    #         "Communication": 0,
    #         "Motricité": 0
    #     }

    #     for tableau in self.deuxieme_tableau:
    #         domaine = tableau['domaine']
    #         domain_results = [r for r in self.resultat_final if r['domaine'] == domaine]
            
    #         # Réinitialiser la somme NS
    #         ns_sum = 0
            
    #         # Remplir les NS par sous-domaine
    #         for result in domain_results:
    #             sous_domain = result['sousdomaine']
                
    #             # Copier la note standard (NS)
    #             if result['ns'] and result['ns'] != '-':
    #                 ns = float(result['ns'])
    #                 tableau[sous_domain] = ns
    #                 if sous_domain in SOUS_DOMAINES[domaine]:
    #                     ns_sum += ns

    #             # Calculer la somme des âges pour les deux premiers domaines
    #             if domaine in ["Communication", "Motricité"]:
    #                 if result.get('age_developpe') and result['age_developpe'] != '-':
    #                     try:
    #                         age = float(result['age_developpe'].replace('<', ''))
    #                         ages_par_domaine[domaine] += age
    #                     except ValueError:
    #                         continue
            
    #         # Mettre à jour la somme NS
    #         tableau['somme_ns'] = ns_sum

    #         # Calculer l'âge développé moyen (somme / 2) pour les deux premiers domaines
    #         if domaine in ["Communication", "Motricité"]:
    #             age_moyen = ages_par_domaine[domaine] / 2 if ages_par_domaine[domaine] > 0 else 0
    #             tableau['age_developpe'] = str(round(age_moyen, 1)) if age_moyen > 0 else '-'
    #         else:
    #             tableau['age_developpe'] = '-'

    #         # Déterminer le percentile
    #         if ns_sum > SEUILS_PERCENTILE.get(domaine, 0):
    #             tableau['percentile'] = '> 99'
    #         else:
    #             try:
    #                 somme_ns = int(ns_sum)
    #                 percentile = self.get_percentile_from_db(domaine, somme_ns)
    #                 if percentile:
    #                     tableau['percentile'] = percentile
    #             except ValueError:
    #                 print(f"Erreur de conversion pour somme_ns: {ns_sum}")

    #         # Déterminer le niveau
    #         if tableau['percentile']:
    #             try:
    #                 percentile_value = float(tableau['percentile'].replace('>', '').replace('<', ''))
    #                 for niveau in self.NIVEAU_DEVELOP:
    #                     if niveau["min"] <= percentile_value <= niveau["max"]:
    #                         tableau['niveau'] = niveau["niveau"]
    #                         break
    #             except ValueError:
    #                 pass

    def calculate_deuxieme_tableau(self):
        print("Starting calculate_deuxieme_tableau")
        
        # Seuils pour les percentiles >99 par domaine
        SEUILS_PERCENTILE = {
            "Communication": 49,
            "Motricité": 42,
            "Comportements inadaptés": 61
        }

        # Mapping des sous-domaines par domaine
        SOUS_DOMAINES = {
            "Communication": ['CVP', 'LE', 'LR'],
            "Motricité": ['MF', 'MG', 'IOM'],
            "Comportements inadaptés": ['EA', 'RS', 'CMC', 'CVC']
        }

        for tableau in self.deuxieme_tableau:
            domaine = tableau['domaine']
            domain_results = [r for r in self.resultat_final if r['domaine'] == domaine]
            
            # Réinitialiser la somme NS
            ns_sum = 0
            age_sum = 0
            
            # Remplir les NS par sous-domaine
            for result in domain_results:
                sous_domain = result['sousdomaine']
                
                # Copier la note standard (NS) pour tous les domaines
                if result['ns'] and result['ns'] != '-':
                    ns = float(result['ns'])
                    tableau[sous_domain] = ns
                    if sous_domain in SOUS_DOMAINES[domaine]:
                        ns_sum += ns

                # Calculer la somme des âges uniquement pour Communication et Motricité
                if domaine in ["Communication", "Motricité"]:
                    if result.get('age_developpe') and result['age_developpe'] != '-':
                        try:
                            age = float(result['age_developpe'].replace('<', ''))
                            age_sum += age
                        except ValueError:
                            continue
            
            # Mettre à jour la somme NS pour tous les domaines
            tableau['somme_ns'] = ns_sum

            # Calculer l'âge développé seulement pour Communication et Motricité
            if domaine in ["Communication", "Motricité"]:
                tableau['age_developpe'] = str(round(age_sum / 2, 1)) if age_sum > 0 else '-'
            else:
                tableau['age_developpe'] = '-'

            # Déterminer le percentile pour tous les domaines
            if ns_sum > SEUILS_PERCENTILE.get(domaine, 0):
                tableau['percentile'] = '> 99'
            else:
                try:
                    somme_ns = int(ns_sum)
                    if domaine == "Comportements inadaptés":
                        domaine = "Comportements"
                    percentile = self.get_percentile_from_db(domaine, somme_ns)
                    print(f"Percentile for {domaine} with NS sum {somme_ns} is {percentile}")
                    if percentile:
                        tableau['percentile'] = percentile
                except ValueError:
                    print(f"Erreur de conversion pour somme_ns: {ns_sum}")

            # Déterminer le niveau pour tous les domaines (y compris Comportements inadaptés)
            if tableau['percentile']:
                try:
                    percentile_value = float(tableau['percentile'].replace('>', '').replace('<', ''))
                    for niveau in self.NIVEAU_DEVELOP:
                        if niveau["min"] <= percentile_value <= niveau["max"]:
                            tableau['niveau'] = niveau["niveau"]
                            break
                except ValueError:
                    pass


    def get_niveau(self, percentile):
        if not percentile or percentile == '-':
            return None
            
        try:
            percentile_value = float(percentile.replace('>', '').replace('<', ''))
        except ValueError:
            return None

        for niveau in self.NIVEAU_DEVELOP:
            if niveau["min"] <= percentile_value <= niveau["max"]:
                return niveau["niveau"]
        return None
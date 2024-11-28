from ..models import StudentScore, Response, ScoreParametrage, AgeTranche

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
        self.deuxieme_tableau = [
            {'domaine': self.DOMAINS["domaine1"], 'CVP': 0, 'LE': 0, 'LR': 0, 'MF': 0, 'MG': 0, 'IOM': 0, 'EA': 0, 'RS': 0, 'CMC': 0, 'CVC': 0, 'somme_ns': 0, 'percentile': '', 'niveau': '', 'age_developpe': ''},
            {'domaine': self.DOMAINS["domaine2"], 'CVP': 0, 'LE': 0, 'LR': 0, 'MF': 0, 'MG': 0, 'IOM': 0, 'EA': 0, 'RS': 0, 'CMC': 0, 'CVC': 0, 'somme_ns': 0, 'percentile': '', 'niveau': '', 'age_developpe': ''},
            {'domaine': self.DOMAINS["domaine3"], 'CVP': 0, 'LE': 0, 'LR': 0, 'MF': 0, 'MG': 0, 'IOM': 0, 'EA': 0, 'RS': 0, 'CMC': 0, 'CVC': 0, 'somme_ns': 0, 'percentile': '', 'niveau': '', 'age_developpe': ''}
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
        responses = Response.objects.filter(questionnaire=self.questionnaire)\
                                  .exclude(question__sous_domain__name='Autre')
        
        # Regrouper les réponses par sous-domaine
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
                result['age_developpe'] = matching_params.age_developpe

    def calculate_deuxieme_tableau(self):
        for result in self.resultat_final:
            domaine = result['domaine']
            sous_domaine = result['sousdomaine']
            ns = result['ns']
            
            for tableau in self.deuxieme_tableau:
                if tableau['domaine'] == domaine:
                    tableau[sous_domaine] = ns
                    tableau['somme_ns'] = sum(
                        float(tableau[sd]) for sd in ['CVP', 'LE', 'LR', 'MF', 'MG', 'IOM', 'EA', 'RS', 'CMC', 'CVC']
                        if tableau[sd] not in ['-', '']
                    )

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

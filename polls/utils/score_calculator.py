from ..models import StudentScore, Response, ScoreParametrage, AgeTranche

class ScoreCalculator:
    NIVEAU_DEVELOP = [
        {"min": 0, "max": 25, "niveau": "Sévère"},
        {"min": 26, "max": 74, "niveau": "Modéré"},
        {"min": 75, "max": 84, "niveau": "Léger"},
        {"min": 85, "max": 1000, "niveau": "Approprié"},
    ]

    def __init__(self, student, questionnaire):
        self.student = student
        self.questionnaire = questionnaire
        self.age_in_months = self.calculate_age_in_months()
        self.tranche = self.get_age_tranche()

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
        responses = Response.objects.filter(
            questionnaire=self.questionnaire
        ).exclude(
            question__sous_domain__domain__name='Autre'
        )

        scores = []
        for response in responses:
            score_param = ScoreParametrage.objects.get(
                tranche=self.tranche,
                domain=response.question.sous_domain.domain.name,
                sous_domain=response.question.sous_domain.name,
                score_brut=response.answer
            )

            niveau = self.get_niveau(score_param.percentile)

            student_score = StudentScore.objects.create(
                student=self.student,
                questionnaire=self.questionnaire,
                domain=response.question.sous_domain.domain.name,
                sous_domain=response.question.sous_domain.name,
                score_brut=response.answer,
                ns=score_param.ns,
                percentile=score_param.percentile,
                niveau=niveau,
                age_developpe=score_param.age_developpe
            )
            scores.append(student_score)

        return scores

    def get_niveau(self, percentile):
        try:
            percentile_value = float(percentile.replace('>', '').replace('<', ''))
        except ValueError:
            return None

        for niveau in self.NIVEAU_DEVELOP:
            if niveau["min"] <= percentile_value <= niveau["max"]:
                return niveau["niveau"]
        return None
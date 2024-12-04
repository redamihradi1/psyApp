from django.db.models import Count, Q ,Case, When, IntegerField, Sum
from itertools import groupby
from collections import defaultdict
from ..models import  ReponseVineland
from polls.models import Questionnaire, Student, Formulaire ,Domain
def calculate_item_plancher(reponses, sous_domaine):
    """Calcule l'item plancher (4 réponses consécutives de 2)"""
    # Trier les réponses par numéro d'item
    items = list(reponses.filter(
        question__sous_domaine=sous_domaine
    ).order_by('question__numero_item'))
    
    consecutive_count = 0
    for reponse in items:
        if reponse.reponse == '2':
            consecutive_count += 1
            if consecutive_count == 4:
                return reponse.question.numero_item - 1
        else:
            consecutive_count = 0
    return 0

def calculate_domain_scores(questionnaire, domain):
    """Calcule tous les scores pour un domaine"""
    scores = {}

    
    for sous_domaine in domain.sous_domaines.all():
        reponses = ReponseVineland.objects.filter(
            questionnaire=questionnaire,
            question__sous_domaine=sous_domaine
        ).order_by('question__numero_item')
        
        # Item plancher
        item_plancher = calculate_item_plancher(reponses, sous_domaine)
        calcul_precedent = item_plancher  * 2

        # Nombre de NSP et sans réponses
        nsp_count = reponses.filter(
            Q(reponse='NSP') | Q(reponse='') | Q(reponse__isnull=True)
        ).count()
        
        # Nombre de N/A
        na_count = reponses.filter(reponse='NA').count()
        
        # Somme des réponses 1 et 2
        sum_1_2 = reponses.filter(
                            question__numero_item__gt=item_plancher
                                ).aggregate(
                                    total=Sum(
                                        Case(
                                            When(reponse='1', then=1),
                                            When(reponse='2', then=2),
                                            default=0,
                                            output_field=IntegerField(),
                                        )
                                    )
                                )['total'] or 0
        
        # Note brute
        note_brute = (item_plancher ) * 2 + sum_1_2 + nsp_count
        

        # Vérifier si le sous-domaine doit être refait
        a_refaire = nsp_count > 2

        scores[sous_domaine.name] = {
            'item_titre': "Entre item plancher et item plafond",
            'item_calcul': f"Item précédent de l'item plancher ({item_plancher }) × 2 = {calcul_precedent}",
            'item_plancher': item_plancher,
            'nsp_count': nsp_count,
            'na_count': na_count,
            'sum_1_2': sum_1_2,
            'note_brute': note_brute,
            'a_refaire': a_refaire  
        }
    
    return scores

def calculate_all_scores(questionnaire):
    """Calcule les scores pour tous les domaines"""
    print('Calcul des scores pour le questionnaire:', questionnaire)
    all_scores = {}
    
    formulaire_domains = questionnaire.formulaire.domains.all()

    for domain in formulaire_domains:
        all_scores[domain.name] = calculate_domain_scores(questionnaire, domain)
        
        # Calcul spécial pour les comportements problématiques
        if domain.name == "Comportements problématiques":
            # Ajouter ici la logique spécifique pour ce domaine
            pass
            
    return all_scores
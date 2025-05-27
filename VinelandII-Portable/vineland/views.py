import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from .models import (
    AgeEquivalentSousDomaine, ComparaisonDomaineVineland, ComparaisonSousDomaineVineland,
    FrequenceDifferenceDomaineVineland, FrequenceDifferenceSousDomaineVineland,
    QuestionVineland, ReponseVineland, PlageItemVineland, EchelleVMapping,
    NoteDomaineVMapping, IntervaleConfianceSousDomaine, IntervaleConfianceDomaine,
    NiveauAdaptatif
)
from django.contrib.auth.models import User
from polls.models import Domain, Formulaire, Student, Questionnaire, SousDomain
from .utils.scoring import calculate_all_scores
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


# ========== FONCTIONS UTILITAIRES ==========

def get_student_age(questionnaire):
    """Calcule l'âge précis de l'étudiant au moment du test."""
    student = questionnaire.student
    
    # Utiliser date_evaluation si elle existe, sinon utiliser created_at
    if questionnaire.date_evaluation:
        date_reference = questionnaire.date_evaluation
    else:
        date_reference = questionnaire.created_at.date()
    
    age_at_test = relativedelta(date_reference, student.date_of_birth)
    
    return {
        'relativedelta': age_at_test,
        'years': age_at_test.years,
        'months': age_at_test.months,
        'days': age_at_test.days,
        'date_reference': date_reference  # Pour debugging/affichage
    }


def get_age_tranches(age_years):
    """Détermine les tranches d'âge pour les différents tableaux."""
    if age_years < 1:
        return None, None
    
    # Tranche d'âge pour les domaines
    if age_years < 3:
        tranche_age = '1-2'
    elif age_years < 7:
        tranche_age = '3-6'
    elif age_years < 19:
        tranche_age = '7-18'
    elif age_years < 50:
        tranche_age = '19-49'
    else:
        tranche_age = '50-90'
    
    # Tranche d'âge pour les intervalles
    if age_years == 1:
        tranche_age_intervalle = '1'
    elif age_years == 2:
        tranche_age_intervalle = '2'
    elif age_years == 3:
        tranche_age_intervalle = '3'
    elif age_years == 4:
        tranche_age_intervalle = '4'
    elif age_years == 5:
        tranche_age_intervalle = '5'
    elif age_years == 6:
        tranche_age_intervalle = '6'
    elif 7 <= age_years <= 8:
        tranche_age_intervalle = '7-8'
    elif 9 <= age_years <= 11:
        tranche_age_intervalle = '9-11'
    elif 12 <= age_years <= 14:
        tranche_age_intervalle = '12-14'
    elif 15 <= age_years <= 18:
        tranche_age_intervalle = '15-18'
    elif 19 <= age_years <= 29:
        tranche_age_intervalle = '19-29'
    elif 30 <= age_years <= 49:
        tranche_age_intervalle = '30-49'
    else:
        tranche_age_intervalle = '50-90'
    
    return tranche_age, tranche_age_intervalle


def find_echelle_v_mapping(sous_domain_obj, note_brute, age_info):
    """Trouve le mapping échelle-v correspondant à la note brute et l'âge."""
    age_years = age_info['years']
    age_months = age_info['months']
    age_days = age_info['days']
    
    mappings = EchelleVMapping.objects.filter(
        sous_domaine=sous_domain_obj,
        note_brute_min__lte=note_brute,
        note_brute_max__gte=note_brute
    )
    
    for mapping in mappings:
        if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
            # Vérification avec jours
            if ((mapping.age_debut_annee < age_years or 
                (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days))):
                if ((mapping.age_fin_annee > age_years or
                    (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                    (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days))):
                    return mapping
        else:
            # Vérification sans jours
            if ((mapping.age_debut_annee < age_years or 
                (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months))):
                if ((mapping.age_fin_annee > age_years or
                    (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months))):
                    return mapping
    return None


def get_domain_mapping(domain_name, domain_note_v_sum, tranche_age):
    """Trouve le mapping de domaine correspondant."""
    filter_kwargs = {'tranche_age': tranche_age}
    
    if 'Communication' in domain_name:
        filter_kwargs.update({
            'communication_min__lte': domain_note_v_sum,
            'communication_max__gte': domain_note_v_sum
        })
    elif 'Vie quotidienne' in domain_name:
        filter_kwargs.update({
            'vie_quotidienne_min__lte': domain_note_v_sum,
            'vie_quotidienne_max__gte': domain_note_v_sum
        })
    elif 'Socialisation' in domain_name:
        filter_kwargs.update({
            'socialisation_min__lte': domain_note_v_sum,
            'socialisation_max__gte': domain_note_v_sum
        })
    elif 'Motricité' in domain_name:
        filter_kwargs.update({
            'motricite_min__lte': domain_note_v_sum,
            'motricite_max__gte': domain_note_v_sum
        })
    
    return NoteDomaineVMapping.objects.filter(**filter_kwargs).first()


def calculate_domain_scores(scores, age_info, tranche_age, tranche_age_intervalle, questionnaire, niveau_confiance=90):
    """Calcule les scores complets pour tous les domaines."""
    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            domain_data = {
                'name': domain_name,
                'name_slug': domain_name.replace(' ', '_'),
                'niveau_confiance': niveau_confiance,
                'sous_domaines': [],
                'domain_score': None
            }
            
            domain_note_v_sum = 0
            
            # Traiter chaque sous-domaine
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Trouver le mapping échelle-v
                echelle_v = find_echelle_v_mapping(sous_domain_obj, score['note_brute'], age_info)
                
                if echelle_v:
                    domain_note_v_sum += echelle_v.note_echelle_v
                    
                    # Ajouter les données du sous-domaine
                    sous_domaine_data = {
                        'name': sous_domain,
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v
                    }
                    
                    # Ajouter l'intervalle de confiance si demandé
                    if niveau_confiance:
                        intervalle = IntervaleConfianceSousDomaine.objects.filter(
                            age=tranche_age_intervalle,
                            niveau_confiance=niveau_confiance,
                            sous_domaine=sous_domain_obj
                        ).first()
                        sous_domaine_data['intervalle'] = intervalle.intervalle if intervalle else None
                    
                    # Ajouter le niveau adaptatif si nécessaire
                    niveau_adaptatif = NiveauAdaptatif.objects.filter(
                        echelle_v_min__lte=echelle_v.note_echelle_v,
                        echelle_v_max__gte=echelle_v.note_echelle_v
                    ).first()
                    if niveau_adaptatif:
                        sous_domaine_data['niveau_adaptatif'] = niveau_adaptatif.get_niveau_display()
                    
                    # Ajouter l'âge équivalent si nécessaire
                    age_equivalent = AgeEquivalentSousDomaine.objects.filter(
                        sous_domaine=sous_domain_obj,
                        note_brute_min__lte=score['note_brute']
                    ).filter(
                        Q(note_brute_max__isnull=True, note_brute_min=score['note_brute']) |
                        Q(note_brute_max__isnull=False, note_brute_max__gte=score['note_brute'])
                    ).first()
                    if age_equivalent:
                        sous_domaine_data['age_equivalent'] = age_equivalent.get_age_equivalent_display()
                    
                    domain_data['sous_domaines'].append(sous_domaine_data)
            
            # Trouver le mapping du domaine
            domain_mapping = get_domain_mapping(domain_name, domain_note_v_sum, tranche_age)
            
            if domain_mapping:
                domain_data['domain_score'] = {
                    'somme_notes_v': domain_note_v_sum,
                    'note_standard': domain_mapping.note_standard,
                    'rang_percentile': domain_mapping.rang_percentile
                }
                
                # Ajouter l'intervalle de confiance du domaine si demandé
                if niveau_confiance:
                    intervalle_domaine = IntervaleConfianceDomaine.objects.filter(
                        age=tranche_age_intervalle,
                        niveau_confiance=niveau_confiance,
                        domain__name=domain_name
                    ).first()
                    if intervalle_domaine:
                        domain_data['domain_score']['intervalle'] = intervalle_domaine.intervalle
                        domain_data['domain_score']['note_composite'] = intervalle_domaine.note_composite
                
                # Ajouter le niveau adaptatif du domaine
                niveau_adaptatif_domain = NiveauAdaptatif.objects.filter(
                    note_standard_min__lte=domain_mapping.note_standard,
                    note_standard_max__gte=domain_mapping.note_standard
                ).first()
                if niveau_adaptatif_domain:
                    domain_data['domain_score']['niveau_adaptatif'] = niveau_adaptatif_domain.get_niveau_display()
            
            complete_scores.append(domain_data)
    
    return complete_scores


def process_questionnaire_responses(request, questions, questionnaire):
    """Traite et sauvegarde les réponses du questionnaire."""
    for key, value in request.session.items():
        if key.startswith('question_'):
            try:
                parts = key.split('_')
                if len(parts) >= 3:
                    sous_domaine_id = int(parts[1])
                    numero_item = int(parts[2])
                    
                    question = QuestionVineland.objects.get(
                        sous_domaine_id=sous_domaine_id,
                        numero_item=numero_item
                    )
                    
                    if isinstance(value, int):
                        value = str(value)
                    
                    valid_values = [str(choice[0]) for choice in QuestionVineland.CHOIX_REPONSES]
                    if value in valid_values or value in ['NSP', 'NA', '?', '']:
                        ReponseVineland.objects.create(
                            question=question,
                            questionnaire=questionnaire,
                            reponse=value
                        )
            except Exception as e:
                print(f"Erreur lors du traitement de la réponse pour la clé {key}: {str(e)}")
                continue


def extract_number(value):
    """Extrait la partie numérique d'une valeur de fréquence."""
    if not value:
        return 9999
    if value.endswith('+'):
        return int(value[:-1])
    elif '-' in value:
        return int(value.split('-')[0])
    else:
        try:
            return int(value)
        except ValueError:
            return 9999


def get_frequency_percentage(difference, freq):
    """Détermine le pourcentage de fréquence basé sur la différence."""
    if not freq:
        return None
    
    if freq.frequence_5 and difference >= extract_number(freq.frequence_5):
        return "5%"
    elif freq.frequence_10 and difference >= extract_number(freq.frequence_10):
        return "10%"
    elif freq.frequence_16 and difference >= extract_number(freq.frequence_16):
        return "16%"
    return None




# ========== VUES PRINCIPALES (REFACTORISÉES) ==========

@login_required
def vineland_questionnaire(request, formulaire_id):
    formulaire = get_object_or_404(Formulaire, id=formulaire_id)
    parent = request.user
    
    if parent.is_superuser:
        students = Student.objects.all()
    else:
        students = Student.objects.filter(parent=parent)
    
    # Récupérer les questions avec leurs relations
    questions = QuestionVineland.objects.select_related(
        'sous_domaine',
        'sous_domaine__domain'
    ).order_by('created_at')

    # Génération d'une clé unique pour chaque question
    for question in questions:
        question.unique_id = f"{question.sous_domaine.id}_{question.numero_item}"

    # Récupérer toutes les plages d'âge
    plages = {
        (plage.sous_domaine_id, plage.item_debut, plage.item_fin): plage 
        for plage in PlageItemVineland.objects.all()
    }

    # Associer les plages d'âge aux questions
    for question in questions:
        for (sous_domaine_id, item_debut, item_fin), plage in plages.items():
            if (question.sous_domaine_id == sous_domaine_id and 
                item_debut <= question.numero_item <= item_fin):
                question.plage_age = plage
                break
        else:
            question.plage_age = None

    paginator = Paginator(questions, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Gérer les données initiales
    initial_data = {}
    if request.session:
        for key in request.session.keys():
            if key.startswith('question_') or key in ['student', 'date_evaluation']:
                initial_data[key] = request.session[key]

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Sauvegarder les réponses dans la session
        for key, value in request.POST.items():
            if key.startswith('question_') or key in ['student', 'date_evaluation']:
                request.session[key] = value

        # Vérifier les questions non répondues sur la page courante
        current_page_questions = page_obj.object_list
        unanswered_current = []
        for question in current_page_questions:
            key = f'question_{question.unique_id}'
            if key not in request.POST:
                unanswered_current.append(f"{question.sous_domaine.name}-{question.numero_item}")

        if unanswered_current:
            messages.info(request, f"Questions sans réponse sur cette page : {', '.join(map(str, unanswered_current))}")

        if action == 'previous':
            prev_page = int(page_number) - 1
            return redirect(f'{request.path}?page={prev_page}')
            
        elif action == 'next':
            next_page = int(page_number) + 1
            return redirect(f'{request.path}?page={next_page}')
            
        elif action == 'submit':
            if 'student' not in request.session:
                messages.error(request, "Veuillez sélectionner un étudiant")
                return redirect(request.path)

            # Vérifier les questions non répondues
            all_unanswered = []
            for question in questions:
                if f'question_{question.unique_id}' not in request.session:
                    all_unanswered.append(f"{question.sous_domaine.name}-{question.numero_item}")

            if all_unanswered:
                messages.warning(request, f"Questions sans réponse dans le questionnaire : {', '.join(map(str, all_unanswered))}")

            student = get_object_or_404(Student, id=request.session['student'])
            
            # Traiter la date d'évaluation
            date_evaluation = None
            if 'date_evaluation' in request.session and request.session['date_evaluation']:
                try:
                    from datetime import datetime
                    date_evaluation = datetime.strptime(request.session['date_evaluation'], '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, "Format de date invalide")
                    return redirect(request.path)
            
            questionnaire = Questionnaire.objects.create(
                formulaire=formulaire,
                student=student,
                parent=parent,
                created_at=timezone.now(),
                date_evaluation=date_evaluation  # NOUVEAU CHAMP
            )
            
            # Traiter les réponses
            process_questionnaire_responses(request, questions, questionnaire)
            
            # Nettoyer la session
            for key in list(request.session.keys()):
                if key.startswith('question_') or key in ['student', 'date_evaluation']:
                    del request.session[key]

            return redirect('vineland:vineland_scores', questionnaire_id=questionnaire.id)

    return render(request, 'vineland/questionnaire.html', {
        'formulaire': formulaire,
        'students': students,
        'page_obj': page_obj,
        'initial_data': initial_data,
    })
@login_required
def vineland_scores(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    
    return render(request, 'vineland/scores.html', {
        'questionnaire': questionnaire,
        'scores': scores
    })


@login_required
def vineland_echelle_v(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    age_info = get_student_age(questionnaire)
    
    echelle_v_scores = {}
    
    for domain_name, domain_scores in scores.items():
        if domain_name != "Comportements problématiques":
            echelle_v_scores[domain_name] = {}
            
            for sous_domain, score in domain_scores.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                echelle_v = find_echelle_v_mapping(sous_domain_obj, score['note_brute'], age_info)
                
                if echelle_v:
                    echelle_v_scores[domain_name][sous_domain] = {
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v
                    }
                else:
                    echelle_v_scores[domain_name][sous_domain] = {
                        'note_brute': score['note_brute'],
                        'note_echelle_v': None,
                        'error': 'Aucune correspondance trouvée'
                    }

    return render(request, 'vineland/echelle_v.html', {
        'questionnaire': questionnaire,
        'echelle_v_scores': echelle_v_scores,
        'age': age_info
    })


@login_required
def vineland_domain_scores(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    age_info = get_student_age(questionnaire)
    tranche_age, _ = get_age_tranches(age_info['years'])
    
    complete_scores = calculate_domain_scores(scores, age_info, tranche_age, None, questionnaire, niveau_confiance=None)
    
    return render(request, 'vineland/domain_scores.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': age_info
    })


@login_required
def vineland_confidence_intervals(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    
    # Récupérer les niveaux de confiance
    domain_confidence_levels = {}
    for key, value in request.GET.items():
        if key.startswith('niveau_confiance_'):
            domain_name = key.replace('niveau_confiance_', '')
            domain_confidence_levels[domain_name] = int(value)
    
    age_info = get_student_age(questionnaire)
    tranche_age, tranche_age_intervalle = get_age_tranches(age_info['years'])
    
    if not tranche_age:
        return render(request, 'vineland/error.html', {'message': 'Âge inférieur à 1 an'})
    
    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            niveau_confiance = domain_confidence_levels.get(domain_name.replace(' ', '_'), 90)
            complete_scores.extend(
                calculate_domain_scores(
                    {domain_name: domain_scores_data}, 
                    age_info, 
                    tranche_age, 
                    tranche_age_intervalle, 
                    questionnaire,
                    niveau_confiance
                )
            )
    
    return render(request, 'vineland/confidence_intervals.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': age_info
    })


@login_required
def vineland_niveaux_adaptatifs(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    
    # Récupérer les niveaux de confiance
    domain_confidence_levels = {}
    for key, value in request.GET.items():
        if key.startswith('niveau_confiance_'):
            domain_name = key.replace('niveau_confiance_', '')
            domain_confidence_levels[domain_name] = int(value)
    
    age_info = get_student_age(questionnaire)
    tranche_age, tranche_age_intervalle = get_age_tranches(age_info['years'])
    
    if not tranche_age:
        return render(request, 'vineland/error.html', {'message': 'Âge inférieur à 1 an'})
    
    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            niveau_confiance = domain_confidence_levels.get(domain_name.replace(' ', '_'), 90)
            complete_scores.extend(
                calculate_domain_scores(
                    {domain_name: domain_scores_data}, 
                    age_info, 
                    tranche_age, 
                    tranche_age_intervalle, 
                    questionnaire,
                    niveau_confiance
                )
            )
    
    return render(request, 'vineland/niveaux_adaptatifs.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': age_info
    })


@login_required
def vineland_age_equivalent(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    
    # Récupérer les niveaux de confiance
    domain_confidence_levels = {}
    for key, value in request.GET.items():
        if key.startswith('niveau_confiance_'):
            domain_name = key.replace('niveau_confiance_', '')
            domain_confidence_levels[domain_name] = int(value)
    
    age_info = get_student_age(questionnaire)
    tranche_age, tranche_age_intervalle = get_age_tranches(age_info['years'])
    
    if not tranche_age:
        return render(request, 'vineland/error.html', {'message': 'Âge inférieur à 1 an'})
    
    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            niveau_confiance = domain_confidence_levels.get(domain_name.replace(' ', '_'), 90)
            complete_scores.extend(
                calculate_domain_scores(
                    {domain_name: domain_scores_data}, 
                    age_info, 
                    tranche_age, 
                    tranche_age_intervalle, 
                    questionnaire,
                    niveau_confiance
                )
            )
    
    return render(request, 'vineland/age_equivalent.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': age_info
    })


@login_required
def vineland_comparaisons_paires(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    
    # Récupérer le niveau de significativité
    niveau_significativite = request.GET.get('niveau_significativite', '.05')
    
    age_info = get_student_age(questionnaire)
    age_years = age_info['years']
    
    # Déterminer les tranches d'âge
    tranche_age, _ = get_age_tranches(age_years)
    
    # Tranche d'âge spécifique pour les comparaisons
    if age_years < 3:
        tranche_age_simple = '1' if age_years < 2 else '2'
    elif age_years < 7:
        tranche_age_simple = str(age_years)
    elif age_years < 9:
        tranche_age_simple = '7-8'
    elif age_years < 12:
        tranche_age_simple = '9-11'
    elif age_years < 15:
        tranche_age_simple = '12-14'
    elif age_years < 19:
        tranche_age_simple = '15-18'
    elif age_years < 30:
        tranche_age_simple = '19-29'
    elif age_years < 50:
        tranche_age_simple = '30-49'
    else:
        tranche_age_simple = '50-90'
    
    # Récupérer les scores
    scores = calculate_all_scores(questionnaire)
    
    # Préparer les structures de données
    domaine_scores = {}
    sous_domaine_scores = {}
    
    # Collecter les scores de domaines et sous-domaines
    for domain_name, domain_data in scores.items():
        if domain_name != "Comportements problématiques":
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                echelle_v = find_echelle_v_mapping(sous_domain_obj, score['note_brute'], age_info)
                
                if echelle_v:
                    sous_domaine_scores[sous_domain] = {
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'domaine': domain_name,
                        'sous_domaine_obj': sous_domain_obj
                    }
                    domain_note_v_sum += echelle_v.note_echelle_v
            
            # Obtenir la note standard du domaine
            domain_mapping = get_domain_mapping(domain_name, domain_note_v_sum, tranche_age)
            if domain_mapping:
                domaine_scores[domain_name] = {
                    'note_standard': domain_mapping.note_standard,
                    'domaine_obj': Domain.objects.get(name=domain_name, formulaire_id=questionnaire.formulaire_id),
                    'somme_notes_v': domain_note_v_sum
                }
    
    # Générer les comparaisons de domaines
    domain_comparisons = generate_domain_comparisons(
        domaine_scores, tranche_age_simple, tranche_age, niveau_significativite
    )
    
    # Générer les comparaisons de sous-domaines par domaine
    sous_domaine_comparisons = generate_sous_domaine_comparisons(
        sous_domaine_scores, tranche_age, niveau_significativite
    )
    
    # Générer les comparaisons inter-domaines
    interdomaine_comparisons = generate_interdomaine_comparisons(
        sous_domaine_scores, tranche_age, niveau_significativite
    )
    
    return render(request, 'vineland/comparaisons_paires.html', {
        'questionnaire': questionnaire,
        'niveau_significativite': niveau_significativite,
        'tranche_age': tranche_age,
        'age': age_info,
        'domain_comparisons': domain_comparisons,
        'sous_domaine_comparisons': sous_domaine_comparisons,
        'interdomaine_comparisons': interdomaine_comparisons,
        'selection_comparisons': []
    })

@login_required
def vineland_export_pdf(request, questionnaire_id):
    """Génère et retourne un PDF avec le rapport d'évaluation Vineland."""
    
    # Récupérer les paramètres d'export depuis la query string
    niveau_confiance = int(request.GET.get('niveau_confiance', 90))
    niveau_significativite = request.GET.get('niveau_significativite', '.05')
    
    # Validation des paramètres
    if niveau_confiance not in [85, 90, 95]:
        niveau_confiance = 90
    if niveau_significativite not in ['.05', '.01']:
        niveau_significativite = '.05'
    
    # Récupérer les données de base
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    student = questionnaire.student
    reponses = ReponseVineland.objects.filter(questionnaire=questionnaire).select_related('question')
    
    # Déterminer les attributs des questions
    text_attr, num_attr = get_question_attributes(reponses)
    
    # Calculer l'âge
    age_info = get_student_age(questionnaire)
    
    # Obtenir les tranches d'âge
    tranche_age, tranche_age_intervalle = get_age_tranches(age_info['years'])
    
    # Préparer la réponse HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vineland_rapport_{student.name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    # Créer le document PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Obtenir les styles
    styles = create_pdf_styles()
    
    # Liste pour stocker tous les éléments du document
    elements = []
    
    # Page 1: Couverture - MODIFIÉE pour inclure les paramètres
    create_cover_page(elements, student, questionnaire, age_info, styles, niveau_confiance, niveau_significativite)
    
    # Page 2: Questions et réponses
    if reponses.exists():
        create_questions_section(elements, reponses, styles, text_attr, num_attr)
    
    # Page 3: Synthèse des scores - MODIFIÉE pour utiliser le niveau de confiance
    scores = calculate_all_scores(questionnaire)
    complete_scores = calculate_domain_scores(
        scores, age_info, tranche_age, tranche_age_intervalle, questionnaire, niveau_confiance
    )
    create_scores_summary(elements, questionnaire, complete_scores, styles)
    
    # Page 4: Comparaisons par paires - MODIFIÉE pour utiliser le niveau de significativité
    create_comparisons_section(elements, questionnaire, scores, age_info, styles, niveau_significativite)
    
    # Construire le PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

# @login_required
# def vineland_export_pdf(request, questionnaire_id):
#     """Génère et retourne un PDF avec le rapport d'évaluation Vineland."""
#     # Récupérer les données de base
#     questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
#     student = questionnaire.student
#     reponses = ReponseVineland.objects.filter(questionnaire=questionnaire).select_related('question')
    
#     # Déterminer les attributs des questions
#     text_attr, num_attr = get_question_attributes(reponses)
    
#     # Calculer l'âge
#     age_info = get_student_age(questionnaire)
    
#     # Obtenir les tranches d'âge
#     tranche_age, tranche_age_intervalle = get_age_tranches(age_info['years'])
    
#     # Préparer la réponse HTTP
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="vineland_rapport_{student.name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
#     # Créer le document PDF
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
#     # Obtenir les styles
#     styles = create_pdf_styles()
    
#     # Liste pour stocker tous les éléments du document
#     elements = []
    
#     # Page 1: Couverture
#     create_cover_page(elements, student, questionnaire, age_info, styles)
    
#     # Page 2: Questions et réponses
#     if reponses.exists():
#         create_questions_section(elements, reponses, styles, text_attr, num_attr)
    
#     # Page 3: Synthèse des scores
#     scores = calculate_all_scores(questionnaire)
#     complete_scores = calculate_domain_scores(
#         scores, age_info, tranche_age, tranche_age_intervalle, questionnaire
#     )
#     create_scores_summary(elements, questionnaire, complete_scores, styles)
    
#     # Page 4: Comparaisons par paires
#     create_comparisons_section(elements, questionnaire, scores, age_info, styles)
    
#     # Construire le PDF
#     doc.build(elements)
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
    
#     return response

# ========== FONCTIONS DE COMPARAISON ==========

def create_pdf_styles():
    """Crée et retourne les styles nécessaires pour le PDF."""
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour les questions
    question_style = ParagraphStyle(
        name='QuestionStyle',
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        wordWrap='CJK',
        alignment=0
    )
    
    # Style pour les cellules compactes
    compact_cell_style = ParagraphStyle(
        name='CompactCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        wordWrap='CJK',
        alignment=0
    )
    
    return {
        'title': styles["Heading1"],
        'subtitle': styles["Heading2"],
        'heading3': styles["Heading3"],
        'normal': styles["Normal"],
        'question': question_style,
        'compact': compact_cell_style
    }


def get_question_attributes(reponses):
    """Détermine les attributs à utiliser pour les questions."""
    if not reponses.exists():
        return None, None
    
    first_question = reponses.first().question
    question_attrs = dir(first_question)
    
    # Déterminer l'attribut pour le texte
    text_attr_options = ['libelle', 'text', 'texte', 'question_text']
    text_attr = next((attr for attr in text_attr_options if attr in question_attrs), None)
    
    # Déterminer l'attribut pour le numéro
    num_attr_options = ['numero_item', 'num_question', 'numero', 'id']
    num_attr = next((attr for attr in num_attr_options if attr in question_attrs), None)
    
    return text_attr, num_attr

def create_cover_page(elements, student, questionnaire, age_info, styles, niveau_confiance=90, niveau_significativite='.05'):
    """Crée la page de couverture du rapport."""
    elements.append(Paragraph("Rapport d'évaluation Vineland-II", styles['title']))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"Enfant: {student.name}", styles['subtitle']))
    elements.append(Paragraph(f"Date de naissance: {student.date_of_birth.strftime('%d/%m/%Y')}", styles['normal']))
    elements.append(Paragraph(
        f"Âge au moment du test: {age_info['years']} ans, {age_info['months']} mois, {age_info['days']} jours",
        styles['normal']
    ))
    elements.append(Paragraph(f"Date d'évaluation: {questionnaire.created_at.strftime('%d/%m/%Y')}", styles['normal']))
    elements.append(Paragraph(
        f"Évaluateur: {questionnaire.parent.get_full_name() or questionnaire.parent.username}",
        styles['normal']
    ))
    
    # NOUVEAU : Ajouter les paramètres d'analyse
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("Paramètres d'analyse", styles['subtitle']))
    elements.append(Paragraph(f"Niveau de confiance: {niveau_confiance}%", styles['normal']))
    elements.append(Paragraph(f"Niveau de significativité: {niveau_significativite}", styles['normal']))
    
    elements.append(PageBreak())
# def create_cover_page(elements, student, questionnaire, age_info, styles):
#     """Crée la page de couverture du rapport."""
#     elements.append(Paragraph("Rapport d'évaluation Vineland-II", styles['title']))
#     elements.append(Spacer(1, 0.5*cm))
#     elements.append(Paragraph(f"Enfant: {student.name}", styles['subtitle']))
#     elements.append(Paragraph(f"Date de naissance: {student.date_of_birth.strftime('%d/%m/%Y')}", styles['normal']))
#     elements.append(Paragraph(
#         f"Âge au moment du test: {age_info['years']} ans, {age_info['months']} mois, {age_info['days']} jours",
#         styles['normal']
#     ))
#     elements.append(Paragraph(f"Date d'évaluation: {questionnaire.created_at.strftime('%d/%m/%Y')}", styles['normal']))
#     elements.append(Paragraph(
#         f"Évaluateur: {questionnaire.parent.get_full_name() or questionnaire.parent.username}",
#         styles['normal']
#     ))
#     elements.append(PageBreak())


def create_questions_section(elements, reponses, styles, text_attr, num_attr):
    """Crée la section des questions et réponses."""
    elements.append(Paragraph("Questions et Réponses", styles['title']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Regrouper les réponses
    grouped_responses = group_responses_by_domain(reponses)
    
    # Créer les tableaux pour chaque domaine
    for domaine, sous_domaines in grouped_responses.items():
        elements.append(Paragraph(f"Domaine: {domaine}", styles['subtitle']))
        
        for sous_domaine, responses in sous_domaines.items():
            create_subdomain_table(elements, domaine, sous_domaine, responses, styles, text_attr, num_attr)
        
        elements.append(Spacer(1, 0.5*cm))
    
    elements.append(PageBreak())


def group_responses_by_domain(reponses):
    """Regroupe les réponses par domaine et sous-domaine."""
    grouped = {}
    for reponse in reponses:
        domaine = reponse.question.sous_domaine.domain.name
        sous_domaine = reponse.question.sous_domaine.name
        
        if domaine not in grouped:
            grouped[domaine] = {}
        if sous_domaine not in grouped[domaine]:
            grouped[domaine][sous_domaine] = []
        
        grouped[domaine][sous_domaine].append(reponse)
    
    return grouped


def create_subdomain_table(elements, domaine, sous_domaine, responses, styles, text_attr, num_attr):
    """Crée un tableau pour un sous-domaine spécifique."""
    elements.append(Paragraph(f"Sous-domaine: {sous_domaine}", styles['heading3']))
    
    # Style unique pour ce sous-domaine
    question_style = ParagraphStyle(
        name=f'QuestionStyle_{domaine}_{sous_domaine}',
        parent=styles['question']
    )
    
    # Préparer les données du tableau
    data = [[
        Paragraph("<b>Item</b>", styles['normal']),
        Paragraph("<b>Question</b>", styles['normal']),
        Paragraph("<b>Réponse</b>", styles['normal'])
    ]]
    
    for idx, reponse in enumerate(responses):
        question_text = safe_get_attr(reponse.question, text_attr, f"Question {idx+1}")
        question_num = safe_get_attr(reponse.question, num_attr, idx+1)
        
        data.append([
            Paragraph(str(question_num), styles['normal']),
            Paragraph(question_text, question_style),
            Paragraph(reponse.reponse, styles['normal'])
        ])
    
    # Créer et styliser le tableau
    table = Table(data, colWidths=[1*cm, 13*cm, 2*cm], repeatRows=1)
    table.setStyle(get_question_table_style())
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))


def safe_get_attr(obj, attr_name, default):
    """Récupère un attribut de manière sécurisée."""
    try:
        return getattr(obj, attr_name, default)
    except (AttributeError, TypeError):
        return default


def get_question_table_style():
    """Retourne le style pour les tableaux de questions."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
    ])


def create_scores_summary(elements, questionnaire, complete_scores, styles):
    """Crée la section de synthèse des scores."""
    elements.append(Paragraph("Synthèse des Résultats", styles['title']))
    elements.append(Spacer(1, 0.5*cm))
    
    for domain in complete_scores:
        elements.append(Paragraph(f"Domaine: {domain['name']}", styles['subtitle']))
        
        # Tableau du score de domaine
        if domain['domain_score']:
            create_domain_score_table(elements, domain)
            elements.append(Spacer(1, 0.5*cm))
        
        # Tableau des sous-domaines
        create_subdomain_score_table(elements, domain)
        elements.append(Spacer(1, 1*cm))
    
    elements.append(PageBreak())


def create_domain_score_table(elements, domain):
    """Crée le tableau des scores de domaine."""
    domain_score_data = [
        ["Somme des notes-V", "Note standard", "Rang percentile", "Niveau adaptatif"],
        [
            str(domain['domain_score']['somme_notes_v']),
            str(domain['domain_score']['note_standard'] or "-"),
            str(domain['domain_score']['rang_percentile'] or "-"),
            domain['domain_score'].get('niveau_adaptatif', 'Non disponible')
        ]
    ]
    
    table = Table(domain_score_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    table.setStyle(get_score_table_style())
    elements.append(table)


def create_subdomain_score_table(elements, domain):
    """Crée le tableau des scores de sous-domaines."""
    data = [["Sous-domaine", "Note brute", "Note échelle-V", "Niveau adaptatif", "Âge équivalent"]]
    
    for sous_domain in domain['sous_domaines']:
        data.append([
            sous_domain['name'],
            str(sous_domain['note_brute']),
            str(sous_domain['note_echelle_v']),
            sous_domain.get('niveau_adaptatif', 'Non disponible'),
            sous_domain.get('age_equivalent', '-')
        ])
    
    table = Table(data, colWidths=[5*cm, 2.5*cm, 2.5*cm, 4*cm, 3*cm])
    table.setStyle(get_score_table_style())
    elements.append(table)


def get_score_table_style():
    """Retourne le style pour les tableaux de scores."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (2, -1), 'CENTER'),
    ])

def create_comparisons_section(elements, questionnaire, scores, age_info, styles, niveau_significativite='.05'):
    """Crée la section des comparaisons par paires."""
    elements.append(Paragraph("Comparaisons par paires", styles['title']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Ajouter une note sur le niveau de significativité utilisé
    elements.append(Paragraph(f"Niveau de significativité utilisé: {niveau_significativite}", styles['normal']))
    elements.append(Spacer(1, 0.3*cm))
    
    tranche_age, _ = get_age_tranches(age_info['years'])
    tranche_age_simple = get_simple_age_range(age_info['years'])
    
    # Collecter les scores
    domaine_scores, sous_domaine_scores = collect_scores_for_comparisons(
        scores, questionnaire, age_info
    )
    
    # Générer et afficher les comparaisons de domaines - AVEC niveau_significativite
    domain_comparisons = generate_domain_comparisons_for_pdf(
        domaine_scores, tranche_age_simple, tranche_age, niveau_significativite
    )
    if domain_comparisons:
        create_domain_comparison_table(elements, domain_comparisons, styles)
        elements.append(Spacer(1, 1*cm))
    
    # Générer et afficher les comparaisons de sous-domaines - AVEC niveau_significativite
    sous_domaine_comparisons = generate_subdomain_comparisons_for_pdf(
        sous_domaine_scores, tranche_age, niveau_significativite
    )
    for domaine, comparisons in sous_domaine_comparisons.items():
        if comparisons:
            create_subdomain_comparison_table(elements, domaine, comparisons, styles)
            elements.append(Spacer(1, 1*cm))
    
    # Générer et afficher les comparaisons inter-domaines - AVEC niveau_significativite
    interdomaine_comparisons = generate_interdomain_comparisons_for_pdf(
        sous_domaine_scores, tranche_age, niveau_significativite
    )
    if interdomaine_comparisons:
        create_interdomain_comparison_table(elements, interdomaine_comparisons, styles)
# def create_comparisons_section(elements, questionnaire, scores, age_info, styles):
#     """Crée la section des comparaisons par paires."""
#     elements.append(Paragraph("Comparaisons par paires", styles['title']))
#     elements.append(Spacer(1, 0.5*cm))
    
#     tranche_age, _ = get_age_tranches(age_info['years'])
#     tranche_age_simple = get_simple_age_range(age_info['years'])
    
#     # Collecter les scores
#     domaine_scores, sous_domaine_scores = collect_scores_for_comparisons(
#         scores, questionnaire, age_info
#     )
    
#     # Générer et afficher les comparaisons de domaines
#     domain_comparisons = generate_domain_comparisons_for_pdf(
#         domaine_scores, tranche_age_simple, tranche_age
#     )
#     if domain_comparisons:
#         create_domain_comparison_table(elements, domain_comparisons, styles)
#         elements.append(Spacer(1, 1*cm))
    
#     # Générer et afficher les comparaisons de sous-domaines
#     sous_domaine_comparisons = generate_subdomain_comparisons_for_pdf(
#         sous_domaine_scores, tranche_age
#     )
#     for domaine, comparisons in sous_domaine_comparisons.items():
#         if comparisons:
#             create_subdomain_comparison_table(elements, domaine, comparisons, styles)
#             elements.append(Spacer(1, 1*cm))
    
#     # Générer et afficher les comparaisons inter-domaines
#     interdomaine_comparisons = generate_interdomain_comparisons_for_pdf(
#         sous_domaine_scores, tranche_age
#     )
#     if interdomaine_comparisons:
#         create_interdomain_comparison_table(elements, interdomaine_comparisons, styles)


def get_simple_age_range(age_years):
    """Détermine la tranche d'âge simple pour les comparaisons."""
    if age_years < 3:
        return '1' if age_years < 2 else '2'
    elif age_years < 7:
        return str(age_years)
    elif age_years < 9:
        return '7-8'
    elif age_years < 12:
        return '9-11'
    elif age_years < 15:
        return '12-14'
    elif age_years < 19:
        return '15-18'
    elif age_years < 30:
        return '19-29'
    elif age_years < 50:
        return '30-49'
    else:
        return '50-90'


def collect_scores_for_comparisons(scores, questionnaire, age_info):
    """Collecte les scores nécessaires pour les comparaisons."""
    domaine_scores = {}
    sous_domaine_scores = {}
    
    for domain_name, domain_data in scores.items():
        if domain_name != "Comportements problématiques":
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                echelle_v = find_echelle_v_mapping(sous_domain_obj, score['note_brute'], age_info)
                
                if echelle_v:
                    sous_domaine_scores[sous_domain] = {
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'domaine': domain_name,
                        'sous_domaine_obj': sous_domain_obj
                    }
                    domain_note_v_sum += echelle_v.note_echelle_v
            
            # Obtenir la note standard du domaine
            tranche_age, _ = get_age_tranches(age_info['years'])
            domain_mapping = get_domain_mapping(domain_name, domain_note_v_sum, tranche_age)
            
            if domain_mapping:
                domaine_scores[domain_name] = {
                    'note_standard': domain_mapping.note_standard,
                    'domaine_obj': Domain.objects.get(
                        name=domain_name,
                        formulaire_id=questionnaire.formulaire_id
                    ),
                    'somme_notes_v': domain_note_v_sum
                }
    
    return domaine_scores, sous_domaine_scores

def generate_domain_comparisons_for_pdf(domaine_scores, tranche_age_simple, tranche_age, niveau_significativite='.05'):
    """Génère les comparaisons de domaines pour le PDF."""
    comparisons = []
    domaines = list(domaine_scores.keys())
    
    for i in range(len(domaines)):
        for j in range(i+1, len(domaines)):
            domaine1 = domaines[i]
            domaine2 = domaines[j]
            score1 = domaine_scores[domaine1]['note_standard']
            score2 = domaine_scores[domaine2]['note_standard']
            
            domain1_obj = domaine_scores[domaine1]['domaine_obj']
            domain2_obj = domaine_scores[domaine2]['domaine_obj']
            
            difference = abs(score1 - score2)
            signe = '>' if score1 > score2 else '<' if score1 < score2 else '='
            
            comparison = find_domain_comparison(
                domain1_obj, domain2_obj, tranche_age_simple, niveau_significativite
            )
            freq = find_domain_frequency(domain1_obj, domain2_obj, tranche_age)
            
            est_significatif = comparison and difference >= comparison.difference_requise
            frequence = get_frequency_percentage(difference, freq)
            
            comparisons.append({
                'domaine1': domaine1,
                'domaine2': domaine2,
                'note1': score1,
                'note2': score2,
                'signe': signe,
                'difference': difference,
                'est_significatif': est_significatif,
                'frequence': frequence
            })
    
    return comparisons
# def generate_domain_comparisons_for_pdf(domaine_scores, tranche_age_simple, tranche_age):
#     """Génère les comparaisons de domaines pour le PDF."""
#     comparisons = []
#     domaines = list(domaine_scores.keys())
#     niveau_significativite = ".05"  # Valeur par défaut
    
#     for i in range(len(domaines)):
#         for j in range(i+1, len(domaines)):
#             domaine1 = domaines[i]
#             domaine2 = domaines[j]
#             score1 = domaine_scores[domaine1]['note_standard']
#             score2 = domaine_scores[domaine2]['note_standard']
            
#             domain1_obj = domaine_scores[domaine1]['domaine_obj']
#             domain2_obj = domaine_scores[domaine2]['domaine_obj']
            
#             difference = abs(score1 - score2)
#             signe = '>' if score1 > score2 else '<' if score1 < score2 else '='
            
#             comparison = find_domain_comparison(
#                 domain1_obj, domain2_obj, tranche_age_simple, niveau_significativite
#             )
#             freq = find_domain_frequency(domain1_obj, domain2_obj, tranche_age)
            
#             est_significatif = comparison and difference >= comparison.difference_requise
#             frequence = get_frequency_percentage(difference, freq)
            
#             comparisons.append({
#                 'domaine1': domaine1,
#                 'domaine2': domaine2,
#                 'note1': score1,
#                 'note2': score2,
#                 'signe': signe,
#                 'difference': difference,
#                 'est_significatif': est_significatif,
#                 'frequence': frequence
#             })
    
#     return comparisons

def generate_subdomain_comparisons_for_pdf(sous_domaine_scores, tranche_age, niveau_significativite='.05'):
    """Génère les comparaisons de sous-domaines pour le PDF."""
    # Grouper par domaine
    grouped = {}
    for sous_domaine, data in sous_domaine_scores.items():
        domaine = data['domaine']
        if domaine not in grouped:
            grouped[domaine] = []
        grouped[domaine].append(sous_domaine)
    
    comparisons = {}
    
    for domaine, sous_domaines in grouped.items():
        comparisons[domaine] = []
        
        for i in range(len(sous_domaines)):
            for j in range(i+1, len(sous_domaines)):
                sous_domaine1 = sous_domaines[i]
                sous_domaine2 = sous_domaines[j]
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                difference = abs(note1 - note2)
                signe = '>' if note1 > note2 else '<' if note1 < note2 else '='
                
                comparison = find_sous_domaine_comparison(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age, niveau_significativite
                )
                freq = find_sous_domaine_frequency(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age
                )
                
                est_significatif = comparison and difference >= comparison.difference_requise
                frequence = get_frequency_percentage(difference, freq)
                
                comparisons[domaine].append({
                    'sous_domaine1': sous_domaine1,
                    'sous_domaine2': sous_domaine2,
                    'note1': note1,
                    'note2': note2,
                    'signe': signe,
                    'difference': difference,
                    'est_significatif': est_significatif,
                    'frequence': frequence
                })
    
    return comparisons

# def generate_subdomain_comparisons_for_pdf(sous_domaine_scores, tranche_age):
#     """Génère les comparaisons de sous-domaines pour le PDF."""
#     # Grouper par domaine
#     grouped = {}
#     for sous_domaine, data in sous_domaine_scores.items():
#         domaine = data['domaine']
#         if domaine not in grouped:
#             grouped[domaine] = []
#         grouped[domaine].append(sous_domaine)
    
#     comparisons = {}
#     niveau_significativite = ".05"
    
#     for domaine, sous_domaines in grouped.items():
#         comparisons[domaine] = []
        
#         for i in range(len(sous_domaines)):
#             for j in range(i+1, len(sous_domaines)):
#                 sous_domaine1 = sous_domaines[i]
#                 sous_domaine2 = sous_domaines[j]
#                 note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
#                 note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
#                 sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
#                 sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
#                 difference = abs(note1 - note2)
#                 signe = '>' if note1 > note2 else '<' if note1 < note2 else '='
                
#                 comparison = find_sous_domaine_comparison(
#                     sous_domaine1_obj, sous_domaine2_obj, tranche_age, niveau_significativite
#                 )
#                 freq = find_sous_domaine_frequency(
#                     sous_domaine1_obj, sous_domaine2_obj, tranche_age
#                 )
                
#                 est_significatif = comparison and difference >= comparison.difference_requise
#                 frequence = get_frequency_percentage(difference, freq)
                
#                 comparisons[domaine].append({
#                     'sous_domaine1': sous_domaine1,
#                     'sous_domaine2': sous_domaine2,
#                     'note1': note1,
#                     'note2': note2,
#                     'signe': signe,
#                     'difference': difference,
#                     'est_significatif': est_significatif,
#                     'frequence': frequence
#                 })
    
#     return comparisons

def generate_interdomain_comparisons_for_pdf(sous_domaine_scores, tranche_age, niveau_significativite='.05'):
    """Génère les comparaisons inter-domaines pour le PDF."""
    comparisons = []
    all_sous_domaines = list(sous_domaine_scores.keys())
    
    for i in range(len(all_sous_domaines)):
        for j in range(i+1, len(all_sous_domaines)):
            sous_domaine1 = all_sous_domaines[i]
            sous_domaine2 = all_sous_domaines[j]
            
            domaine1 = sous_domaine_scores[sous_domaine1]['domaine']
            domaine2 = sous_domaine_scores[sous_domaine2]['domaine']
            
            if domaine1 != domaine2:
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                difference = abs(note1 - note2)
                signe = '>' if note1 > note2 else '<' if note1 < note2 else '='
                
                comparison = find_sous_domaine_comparison(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age, niveau_significativite
                )
                freq = find_sous_domaine_frequency(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age
                )
                
                est_significatif = comparison and difference >= comparison.difference_requise
                frequence = get_frequency_percentage(difference, freq)
                
                comparisons.append({
                    'sous_domaine1': sous_domaine1,
                    'sous_domaine2': sous_domaine2,
                    'domaine1': domaine1,
                    'domaine2': domaine2,
                    'note1': note1,
                    'note2': note2,
                    'signe': signe,
                    'difference': difference,
                    'est_significatif': est_significatif,
                    'frequence': frequence
                })
    
    return comparisons
# def generate_interdomain_comparisons_for_pdf(sous_domaine_scores, tranche_age):
#     """Génère les comparaisons inter-domaines pour le PDF."""
#     comparisons = []
#     all_sous_domaines = list(sous_domaine_scores.keys())
#     niveau_significativite = ".05"
    
#     for i in range(len(all_sous_domaines)):
#         for j in range(i+1, len(all_sous_domaines)):
#             sous_domaine1 = all_sous_domaines[i]
#             sous_domaine2 = all_sous_domaines[j]
            
#             domaine1 = sous_domaine_scores[sous_domaine1]['domaine']
#             domaine2 = sous_domaine_scores[sous_domaine2]['domaine']
            
#             if domaine1 != domaine2:
#                 note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
#                 note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
#                 sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
#                 sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
#                 difference = abs(note1 - note2)
#                 signe = '>' if note1 > note2 else '<' if note1 < note2 else '='
                
#                 comparison = find_sous_domaine_comparison(
#                     sous_domaine1_obj, sous_domaine2_obj, tranche_age, niveau_significativite
#                 )
#                 freq = find_sous_domaine_frequency(
#                     sous_domaine1_obj, sous_domaine2_obj, tranche_age
#                 )
                
#                 est_significatif = comparison and difference >= comparison.difference_requise
#                 frequence = get_frequency_percentage(difference, freq)
                
#                 comparisons.append({
#                     'sous_domaine1': sous_domaine1,
#                     'sous_domaine2': sous_domaine2,
#                     'domaine1': domaine1,
#                     'domaine2': domaine2,
#                     'note1': note1,
#                     'note2': note2,
#                     'signe': signe,
#                     'difference': difference,
#                     'est_significatif': est_significatif,
#                     'frequence': frequence
#                 })
    
#     return comparisons


def create_domain_comparison_table(elements, comparisons, styles):
    """Crée le tableau des comparaisons de domaines."""
    elements.append(Paragraph("Comparaisons des domaines", styles['subtitle']))
    
    data = [["Domaine 1", "Note", "<, >, ou =", "Note", "Domaine 2", "Différence", "Significatif", "Fréquence"]]
    
    for comp in comparisons:
        data.append([
            comp['domaine1'],
            str(comp['note1']),
            comp['signe'],
            str(comp['note2']),
            comp['domaine2'],
            str(comp['difference']),
            "✓" if comp['est_significatif'] else "-",
            comp['frequence'] if comp['frequence'] else "-"
        ])
    
    table = Table(data, colWidths=[3*cm, 1.5*cm, 1.5*cm, 1.5*cm, 3*cm, 2*cm, 2*cm, 2*cm])
    table.setStyle(get_comparison_table_style())
    elements.append(table)


def create_subdomain_comparison_table(elements, domaine, comparisons, styles):
    """Crée le tableau des comparaisons de sous-domaines."""
    elements.append(Paragraph(f"Comparaisons des sous-domaines - {domaine}", styles['subtitle']))
    
    data = [["Sous-domaine 1", "Note", "<, >, ou =", "Note", "Sous-domaine 2", "Différence", "Significatif", "Fréquence"]]
    
    for comp in comparisons:
        data.append([
            comp['sous_domaine1'],
            str(comp['note1']),
            comp['signe'],
            str(comp['note2']),
            comp['sous_domaine2'],
            str(comp['difference']),
            "✓" if comp['est_significatif'] else "-",
            comp['frequence'] if comp['frequence'] else "-"
        ])
    
    table = Table(data, colWidths=[3*cm, 1.5*cm, 1.5*cm, 1.5*cm, 3*cm, 2*cm, 2*cm, 2*cm])
    table.setStyle(get_comparison_table_style())
    elements.append(table)


def create_interdomain_comparison_table(elements, comparisons, styles):
    """Crée le tableau des comparaisons inter-domaines."""
    elements.append(Paragraph("Comparaisons des sous-domaines inter-domaines", styles['subtitle']))
    
    data = [[
        Paragraph("<b>Sous-domaine 1</b>", styles['compact']),
        Paragraph("<b>Domaine</b>", styles['compact']),
        Paragraph("<b>Note</b>", styles['compact']),
        Paragraph("<b><, >, =</b>", styles['compact']),
        Paragraph("<b>Note</b>", styles['compact']),
        Paragraph("<b>Sous-domaine 2</b>", styles['compact']),
        Paragraph("<b>Domaine</b>", styles['compact']),
        Paragraph("<b>Diff.</b>", styles['compact']),
        Paragraph("<b>Signif.</b>", styles['compact']),
        Paragraph("<b>Fréq.</b>", styles['compact'])
    ]]
    
    for comp in comparisons:
        data.append([
            Paragraph(comp['sous_domaine1'], styles['compact']),
            Paragraph(comp['domaine1'], styles['compact']),
            Paragraph(str(comp['note1']), styles['compact']),
            Paragraph(comp['signe'], styles['compact']),
            Paragraph(str(comp['note2']), styles['compact']),
            Paragraph(comp['sous_domaine2'], styles['compact']),
            Paragraph(comp['domaine2'], styles['compact']),
            Paragraph(str(comp['difference']), styles['compact']),
            Paragraph("✓" if comp['est_significatif'] else "-", styles['compact']),
            Paragraph(comp['frequence'] if comp['frequence'] else "-", styles['compact'])
        ])
    
    table = Table(data, colWidths=[2.5*cm, 2.5*cm, 1*cm, 1*cm, 1*cm, 2.5*cm, 2.5*cm, 1.5*cm, 1.5*cm, 1.5*cm])
    table.setStyle(get_comparison_table_style())
    elements.append(table)


def get_comparison_table_style():
    """Retourne le style pour les tableaux de comparaisons."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (3, -1), 'CENTER'),
        ('ALIGN', (5, 1), (7, -1), 'CENTER'),
        ('BACKGROUND', (2, 1), (2, -1), colors.lightgrey),
    ])


def generate_domain_comparisons(domaine_scores, tranche_age_simple, tranche_age, niveau_significativite):
    """Génère les comparaisons par paires pour les domaines."""
    domain_comparisons = []
    domaines = list(domaine_scores.keys())
    
    for i in range(len(domaines)):
        for j in range(i+1, len(domaines)):
            domaine1 = domaines[i]
            domaine2 = domaines[j]
            score1 = domaine_scores[domaine1]['note_standard']
            score2 = domaine_scores[domaine2]['note_standard']
            
            domain1_obj = domaine_scores[domaine1]['domaine_obj']
            domain2_obj = domaine_scores[domaine2]['domaine_obj']
            
            difference = abs(score1 - score2)
            signe = '>' if score1 > score2 else '<' if score1 < score2 else '='
            
            # Rechercher la comparaison
            comparison = find_domain_comparison(
                domain1_obj, domain2_obj, tranche_age_simple, niveau_significativite
            )
            
            # Rechercher les fréquences
            freq = find_domain_frequency(domain1_obj, domain2_obj, tranche_age)
            
            est_significatif = comparison and difference >= comparison.difference_requise
            frequence = get_frequency_percentage(difference, freq)
            
            domain_comparisons.append({
                'domaine1': domaine1,
                'domaine2': domaine2,
                'note1': score1,
                'note2': score2,
                'signe': signe,
                'difference': difference,
                'difference_requise': comparison.difference_requise if comparison else None,
                'est_significatif': est_significatif,
                'frequence': frequence
            })
    
    return domain_comparisons


def generate_sous_domaine_comparisons(sous_domaine_scores, tranche_age, niveau_significativite):
    """Génère les comparaisons par paires pour les sous-domaines, groupées par domaine."""
    # Grouper les sous-domaines par domaine
    sous_domaine_grouped = {}
    for sous_domaine, data in sous_domaine_scores.items():
        domaine = data['domaine']
        if domaine not in sous_domaine_grouped:
            sous_domaine_grouped[domaine] = []
        sous_domaine_grouped[domaine].append(sous_domaine)
    
    sous_domaine_comparisons = {}
    
    for domaine, sous_domaines in sous_domaine_grouped.items():
        sous_domaine_comparisons[domaine] = []
        
        for i in range(len(sous_domaines)):
            for j in range(i+1, len(sous_domaines)):
                sous_domaine1 = sous_domaines[i]
                sous_domaine2 = sous_domaines[j]
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                difference = abs(note1 - note2)
                signe = '>' if note1 > note2 else '<' if note1 < note2 else '='
                
                # Rechercher la comparaison
                comparison = find_sous_domaine_comparison(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age, niveau_significativite
                )
                
                # Rechercher les fréquences
                freq = find_sous_domaine_frequency(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age
                )
                
                est_significatif = comparison and difference >= comparison.difference_requise
                frequence = get_frequency_percentage(difference, freq)
                
                sous_domaine_comparisons[domaine].append({
                    'sous_domaine1': sous_domaine1,
                    'sous_domaine2': sous_domaine2,
                    'note1': note1,
                    'note2': note2,
                    'signe': signe,
                    'difference': difference,
                    'difference_requise': comparison.difference_requise if comparison else None,
                    'est_significatif': est_significatif,
                    'frequence': frequence
                })
    
    return sous_domaine_comparisons


def generate_interdomaine_comparisons(sous_domaine_scores, tranche_age, niveau_significativite):
    """Génère les comparaisons inter-domaines pour les sous-domaines."""
    interdomaine_comparisons = []
    all_sous_domaines = list(sous_domaine_scores.keys())
    
    for i in range(len(all_sous_domaines)):
        for j in range(i+1, len(all_sous_domaines)):
            sous_domaine1 = all_sous_domaines[i]
            sous_domaine2 = all_sous_domaines[j]
            
            domaine1 = sous_domaine_scores[sous_domaine1]['domaine']
            domaine2 = sous_domaine_scores[sous_domaine2]['domaine']
            
            # Seulement si domaines différents
            if domaine1 != domaine2:
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                difference = abs(note1 - note2)
                signe = '>' if note1 > note2 else '<' if note1 < note2 else '='
                
                # Rechercher la comparaison
                comparison = find_sous_domaine_comparison(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age, niveau_significativite
                )
                
                # Rechercher les fréquences
                freq = find_sous_domaine_frequency(
                    sous_domaine1_obj, sous_domaine2_obj, tranche_age
                )
                
                est_significatif = comparison and difference >= comparison.difference_requise
                frequence = get_frequency_percentage(difference, freq)
                
                interdomaine_comparisons.append({
                    'sous_domaine1': sous_domaine1,
                    'sous_domaine2': sous_domaine2,
                    'domaine1': domaine1,
                    'domaine2': domaine2,
                    'note1': note1,
                    'note2': note2,
                    'signe': signe,
                    'difference': difference,
                    'difference_requise': comparison.difference_requise if comparison else None,
                    'est_significatif': est_significatif,
                    'frequence': frequence
                })
    
    return interdomaine_comparisons


def find_domain_comparison(domain1_obj, domain2_obj, tranche_age, niveau_significativite):
    """Trouve la comparaison entre deux domaines."""
    try:
        return ComparaisonDomaineVineland.objects.get(
            age=tranche_age,
            niveau_significativite=niveau_significativite,
            domaine1=domain1_obj,
            domaine2=domain2_obj
        )
    except ComparaisonDomaineVineland.DoesNotExist:
        try:
            return ComparaisonDomaineVineland.objects.get(
                age=tranche_age,
                niveau_significativite=niveau_significativite,
                domaine1=domain2_obj,
                domaine2=domain1_obj
            )
        except ComparaisonDomaineVineland.DoesNotExist:
            return None


def find_domain_frequency(domain1_obj, domain2_obj, tranche_age):
    """Trouve les fréquences de différence entre deux domaines."""
    try:
        return FrequenceDifferenceDomaineVineland.objects.get(
            age=tranche_age,
            domaine1=domain1_obj,
            domaine2=domain2_obj
        )
    except FrequenceDifferenceDomaineVineland.DoesNotExist:
        try:
            return FrequenceDifferenceDomaineVineland.objects.get(
                age=tranche_age,
                domaine1=domain2_obj,
                domaine2=domain1_obj
            )
        except FrequenceDifferenceDomaineVineland.DoesNotExist:
            return None


def find_sous_domaine_comparison(sous_domaine1_obj, sous_domaine2_obj, tranche_age, niveau_significativite):
    """Trouve la comparaison entre deux sous-domaines."""
    try:
        return ComparaisonSousDomaineVineland.objects.get(
            age=tranche_age,
            niveau_significativite=niveau_significativite,
            sous_domaine1=sous_domaine1_obj,
            sous_domaine2=sous_domaine2_obj
        )
    except ComparaisonSousDomaineVineland.DoesNotExist:
        try:
            return ComparaisonSousDomaineVineland.objects.get(
                age=tranche_age,
                niveau_significativite=niveau_significativite,
                sous_domaine1=sous_domaine2_obj,
                sous_domaine2=sous_domaine1_obj
            )
        except ComparaisonSousDomaineVineland.DoesNotExist:
            return None


def find_sous_domaine_frequency(sous_domaine1_obj, sous_domaine2_obj, tranche_age):
    """Trouve les fréquences de différence entre deux sous-domaines."""
    try:
        return FrequenceDifferenceSousDomaineVineland.objects.get(
            age=tranche_age,
            sous_domaine1=sous_domaine1_obj,
            sous_domaine2=sous_domaine2_obj
        )
    except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
        try:
            return FrequenceDifferenceSousDomaineVineland.objects.get(
                age=tranche_age,
                sous_domaine1=sous_domaine2_obj,
                sous_domaine2=sous_domaine1_obj
            )
        except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
            return None
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from .models import AgeEquivalentSousDomaine, ComparaisonDomaineVineland, ComparaisonSousDomaineVineland, FrequenceDifferenceDomaineVineland, FrequenceDifferenceSousDomaineVineland, QuestionVineland, ReponseVineland , PlageItemVineland , EchelleVMapping , NoteDomaineVMapping , IntervaleConfianceSousDomaine , IntervaleConfianceDomaine , NiveauAdaptatif 
from django.contrib.auth.models import User
from polls.models import Domain, Formulaire, Student, Questionnaire , SousDomain
from .utils.scoring import calculate_all_scores
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
from django.views.decorators.http import require_http_methods



@login_required
def vineland_questionnaire(request, formulaire_id):
    formulaire = get_object_or_404(Formulaire, id=formulaire_id)
    parent = request.user
    
    if parent.is_superuser:
        students = Student.objects.all()
    else:
        students = Student.objects.filter(parent=parent)
    
    # Récupérer les questions avec leurs relations  10 question pour le test
    questions = QuestionVineland.objects.select_related(
        'sous_domaine',
        'sous_domaine__domain'
    ).order_by(
        'created_at'  # Utilisation du timestamp de création pour l'ordre
    )


    # Génération d'une clé unique pour chaque question
    for question in questions:
        # Créer un identifiant unique qui combine sous_domaine et numero_item
        question.unique_id = f"{question.sous_domaine.id}_{question.numero_item}"

    # Récupérer toutes les plages d'âge en une seule requête
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

    # Gérer les données initiales avec les nouveaux identifiants uniques
    initial_data = {}
    if request.session:
        for key in request.session.keys():
            if key.startswith('question_') or key == 'student':
                initial_data[key] = request.session[key]

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Sauvegarder les réponses dans la session avec les identifiants uniques
        for key, value in request.POST.items():
            if key.startswith('question_') or key == 'student':
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
            print('submit')
            if 'student' not in request.session:
                messages.error(request, "Veuillez sélectionner un étudiant")
                return redirect(request.path)

            # Vérifier les questions non répondues avec les identifiants uniques
            all_unanswered = []
            for question in questions:
                if f'question_{question.unique_id}' not in request.session:
                    all_unanswered.append(f"{question.sous_domaine.name}-{question.numero_item}")

            if all_unanswered:
                messages.warning(request, f"Questions sans réponse dans le questionnaire : {', '.join(map(str, all_unanswered))}")

            student = get_object_or_404(Student, id=request.session['student'])
            questionnaire = Questionnaire.objects.create(
                formulaire=formulaire,
                student=student,
                parent=parent,
                created_at=timezone.now(),
            )
            # Traiter les réponses avec les identifiants uniques
            for key, value in request.session.items():
                if key.startswith('question_'):
                    try:
                        # La clé est au format "question_sous_domaine_id_numero_item"
                        parts = key.split('_')
                        if len(parts) >= 3:  # Vérifie qu'on a tous les éléments nécessaires
                            sous_domaine_id = int(parts[1])
                            numero_item = int(parts[2])
                            
                            # Récupérer la question correspondante
                            question = QuestionVineland.objects.get(
                                sous_domaine_id=sous_domaine_id,
                                numero_item=numero_item
                            )
                            
                            if isinstance(value, int):
                                value = str(value)
                            
                            # Vérifier si la valeur est valide
                            valid_values = [str(choice[0]) for choice in QuestionVineland.CHOIX_REPONSES]
                            if value in valid_values or value in ['NSP', 'NA', '?', '']:
                                reponse = ReponseVineland(
                                    question=question,
                                    questionnaire=questionnaire,
                                    reponse=value
                                )
                                reponse.save()
                    except Exception as e:
                        # Log l'erreur ou gérer l'exception comme nécessaire
                        print(f"Erreur lors du traitement de la réponse pour la clé {key}: {str(e)}")
                        continue
                        # Nettoyer la session
            
            for key in list(request.session.keys()):
                if key.startswith('question_') or key == 'student':
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
    student = questionnaire.student
    
    age_at_test = relativedelta(questionnaire.created_at.date(), student.date_of_birth)
    age_years = age_at_test.years
    age_months = age_at_test.months
    age_days = age_at_test.days

    print(f"Âge de l'enfant: {age_years}a {age_months}m {age_days}j")

    echelle_v_scores = {}
    
    for domain_name, domain_scores in scores.items():
        if domain_name != "Comportements problématiques":
            echelle_v_scores[domain_name] = {}
            
            for sous_domain, score in domain_scores.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                print(f"\n=== {sous_domain} ===")
                print(f"Note brute: {score['note_brute']}")

                # D'abord filtrer par note brute
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )

                # Trouver la bonne correspondance d'âge
                echelle_v = None
                for mapping in mappings:
                    # Si l'intervalle a des jours (format Y;M;D)
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        # Comparer les dates complètes Y;M;D
                        if (mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days)):
                            if (mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days)):
                                echelle_v = mapping
                                break
                    else:
                        # Format Y;M - comparer seulement années et mois
                        if (mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months)):
                            if (mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months)):
                                echelle_v = mapping
                                break

                if echelle_v:
                    print(f"✅ Correspondance trouvée: {echelle_v.age_debut_annee};{echelle_v.age_debut_mois} à {echelle_v.age_fin_annee};{echelle_v.age_fin_mois}")
                    echelle_v_scores[domain_name][sous_domain] = {
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v
                    }
                else:
                    print(f"❌ Aucune correspondance trouvée pour la note {score['note_brute']}")
                    echelle_v_scores[domain_name][sous_domain] = {
                        'note_brute': score['note_brute'],
                        'note_echelle_v': None,
                        'error': 'Aucune correspondance trouvée'
                    }

    return render(request, 'vineland/echelle_v.html', {
        'questionnaire': questionnaire,
        'echelle_v_scores': echelle_v_scores,
        'age': {
            'years': age_years,
            'months': age_months,
            'days': age_days
        }
    })



@login_required
def vineland_domain_scores(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    student = questionnaire.student
    
    # Utiliser relativedelta pour un calcul précis de l'âge
    age_at_test = relativedelta(questionnaire.created_at.date(), student.date_of_birth)
    age_years = age_at_test.years
    age_months = age_at_test.months
    age_days = age_at_test.days
    
    # Déterminer la tranche d'âge
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

    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            domain_data = {
                'name': domain_name,
                'sous_domaines': [],
                'domain_score': None
            }
            
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Recherche des mappings correspondant à la note brute
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )

                # Recherche de la correspondance d'âge
                echelle_v = None
                for mapping in mappings:
                    # Vérification avec jours si présents
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        if ((mapping.age_debut_annee < age_years) or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days)):
                            if ((mapping.age_fin_annee > age_years) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days)):
                                echelle_v = mapping
                                break
                    else:
                        # Vérification sans jours
                        if ((mapping.age_debut_annee < age_years) or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months)):
                            if ((mapping.age_fin_annee > age_years) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months)):
                                echelle_v = mapping
                                break
                
                if echelle_v:
                    domain_note_v_sum += echelle_v.note_echelle_v
                    domain_data['sous_domaines'].append({
                        'name': sous_domain,
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v
                    })
            
            # Construction des filtres pour le domaine
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

            domain_mapping = NoteDomaineVMapping.objects.filter(**filter_kwargs).first()
            
            if domain_mapping:
                domain_data['domain_score'] = {
                    'somme_notes_v': domain_note_v_sum,
                    'note_standard': domain_mapping.note_standard,
                    'rang_percentile': domain_mapping.rang_percentile
                }
            
            complete_scores.append(domain_data)
    
    return render(request, 'vineland/domain_scores.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': {
            'years': age_years,
            'months': age_months,
            'days': age_days
        }
    })




@login_required
def vineland_confidence_intervals(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    student = questionnaire.student
    
    # Récupérer les niveaux de confiance
    domain_confidence_levels = {}
    for key, value in request.GET.items():
        if key.startswith('niveau_confiance_'):
            domain_name = key.replace('niveau_confiance_', '')
            domain_confidence_levels[domain_name] = int(value)
    
    # Calcul précis de l'âge avec relativedelta
    age_at_test = relativedelta(questionnaire.created_at.date(), student.date_of_birth)
    age_years = age_at_test.years
    age_months = age_at_test.months
    age_days = age_at_test.days
    
    # Déterminer les tranches d'âge
    if age_years < 1:
        return "< 1 an"
    elif age_years == 1:
        tranche_age = '1'
        tranche_age_intervalle = '1'
    elif age_years == 2:
        tranche_age = '2'
        tranche_age_intervalle = '2'
    elif age_years == 3:
        tranche_age = '3'
        tranche_age_intervalle = '3'
    elif age_years == 4:
        tranche_age = '4'
        tranche_age_intervalle = '4'
    elif age_years == 5:
        tranche_age = '5'
        tranche_age_intervalle = '5'
    elif age_years == 6:
        tranche_age = '6'
        tranche_age_intervalle = '6'
    elif 7 <= age_years <= 8:
        tranche_age = '7-8'
        tranche_age_intervalle = '7-8'
    elif 9 <= age_years <= 11:
        tranche_age = '9-11'
        tranche_age_intervalle = '9-11'
    elif 12 <= age_years <= 14:
        tranche_age = '12-14'
        tranche_age_intervalle = '12-14'
    elif 15 <= age_years <= 18:
        tranche_age = '15-18'
        tranche_age_intervalle = '15-18'
    elif 19 <= age_years <= 29:
        tranche_age = '19-29'
        tranche_age_intervalle = '19-29'
    elif 30 <= age_years <= 49:
        tranche_age = '30-49'
        tranche_age_intervalle = '30-49'
    elif age_years >= 50:
        tranche_age = '50-90'
        tranche_age_intervalle = '50-90'


    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            niveau_confiance = domain_confidence_levels.get(domain_name.replace(' ', '_'), 90)
            
            domain_data = {
                'name': domain_name,
                'name_slug': domain_name.replace(' ', '_'),
                'niveau_confiance': niveau_confiance,
                'sous_domaines': [],
                'domain_score': None
            }
            
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Recherche des mappings correspondant à la note brute
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )

                # Recherche de la correspondance d'âge
                echelle_v = None
                for mapping in mappings:
                    # Vérification avec jours si présents
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days))):
                                echelle_v = mapping
                                break
                    else:
                        # Vérification sans jours
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months))):
                                echelle_v = mapping
                                break
                
                # Obtenir l'intervalle de confiance du sous-domaine
                intervalle_sous_domaine = IntervaleConfianceSousDomaine.objects.filter(
                    age=tranche_age_intervalle,
                    niveau_confiance=niveau_confiance,
                    sous_domaine=sous_domain_obj
                ).first()
                
                if echelle_v:
                    domain_note_v_sum += echelle_v.note_echelle_v
                    domain_data['sous_domaines'].append({
                        'name': sous_domain,
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'intervalle': intervalle_sous_domaine.intervalle if intervalle_sous_domaine else None
                    })
            
            # Construction des filtres pour le domaine
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

            domain_mapping = NoteDomaineVMapping.objects.filter(**filter_kwargs).first()
            intervalle_domaine = IntervaleConfianceDomaine.objects.filter(
                age=tranche_age_intervalle,
                niveau_confiance=niveau_confiance,
                domain__name=domain_name
            ).first()
            
            if domain_mapping:
                domain_data['domain_score'] = {
                    'somme_notes_v': domain_note_v_sum,
                    'note_standard': domain_mapping.note_standard,
                    'rang_percentile': domain_mapping.rang_percentile,
                    'intervalle': intervalle_domaine.intervalle if intervalle_domaine else None,
                    'note_composite': intervalle_domaine.note_composite if intervalle_domaine else None
                }
            
            complete_scores.append(domain_data)
    
    return render(request, 'vineland/confidence_intervals.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': {
            'years': age_years,
            'months': age_months,
            'days': age_days
        }
    })

@login_required
def vineland_niveaux_adaptatifs(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    student = questionnaire.student
    
    # Récupérer les niveaux de confiance
    domain_confidence_levels = {}
    for key, value in request.GET.items():
        if key.startswith('niveau_confiance_'):
            domain_name = key.replace('niveau_confiance_', '')
            domain_confidence_levels[domain_name] = int(value)
    
    # Calcul précis de l'âge avec relativedelta
    age_at_test = relativedelta(questionnaire.created_at.date(), student.date_of_birth)
    age_years = age_at_test.years
    age_months = age_at_test.months
    age_days = age_at_test.days
    
    # Déterminer les tranches d'âge
    if age_years < 1:
        return "< 1 an"
    elif age_years == 1:
        tranche_age = '1'
        tranche_age_intervalle = '1'
    elif age_years == 2:
        tranche_age = '2'
        tranche_age_intervalle = '2'
    elif age_years == 3:
        tranche_age = '3'
        tranche_age_intervalle = '3'
    elif age_years == 4:
        tranche_age = '4'
        tranche_age_intervalle = '4'
    elif age_years == 5:
        tranche_age = '5'
        tranche_age_intervalle = '5'
    elif age_years == 6:
        tranche_age = '6'
        tranche_age_intervalle = '6'
    elif 7 <= age_years <= 8:
        tranche_age = '7-8'
        tranche_age_intervalle = '7-8'
    elif 9 <= age_years <= 11:
        tranche_age = '9-11'
        tranche_age_intervalle = '9-11'
    elif 12 <= age_years <= 14:
        tranche_age = '12-14'
        tranche_age_intervalle = '12-14'
    elif 15 <= age_years <= 18:
        tranche_age = '15-18'
        tranche_age_intervalle = '15-18'
    elif 19 <= age_years <= 29:
        tranche_age = '19-29'
        tranche_age_intervalle = '19-29'
    elif 30 <= age_years <= 49:
        tranche_age = '30-49'
        tranche_age_intervalle = '30-49'
    elif age_years >= 50:
        tranche_age = '50-90'
        tranche_age_intervalle = '50-90'



    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            niveau_confiance = domain_confidence_levels.get(domain_name.replace(' ', '_'), 90)
            
            domain_data = {
                'name': domain_name,
                'name_slug': domain_name.replace(' ', '_'),
                'niveau_confiance': niveau_confiance,
                'sous_domaines': [],
                'domain_score': None
            }
            
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Recherche des mappings correspondant à la note brute
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )

                # Recherche de la correspondance d'âge
                echelle_v = None
                for mapping in mappings:
                    # Vérification avec jours si présents
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days))):
                                echelle_v = mapping
                                break
                    else:
                        # Vérification sans jours
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months))):
                                echelle_v = mapping
                                break
                
                # Obtenir l'intervalle de confiance
                intervalle = IntervaleConfianceSousDomaine.objects.filter(
                    age=tranche_age_intervalle,
                    niveau_confiance=niveau_confiance,
                    sous_domaine=sous_domain_obj
                ).first()
                
                if echelle_v:
                    domain_note_v_sum += echelle_v.note_echelle_v
                    
                    # Trouver le niveau adaptatif pour le sous-domaine
                    niveau_adaptatif = NiveauAdaptatif.objects.filter(
                        echelle_v_min__lte=echelle_v.note_echelle_v,
                        echelle_v_max__gte=echelle_v.note_echelle_v
                    ).first()
                    
                    domain_data['sous_domaines'].append({
                        'name': sous_domain,
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'intervalle': intervalle.intervalle if intervalle else None,
                        'niveau_adaptatif': niveau_adaptatif.get_niveau_display() if niveau_adaptatif else None
                    })
            
            # Construction des filtres pour le domaine
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

            domain_mapping = NoteDomaineVMapping.objects.filter(**filter_kwargs).first()
            intervalle_domaine = IntervaleConfianceDomaine.objects.filter(
                age=tranche_age_intervalle,
                niveau_confiance=niveau_confiance,
                domain__name=domain_name
            ).first()
            
            if domain_mapping:
                niveau_adaptatif = NiveauAdaptatif.objects.filter(
                    note_standard_min__lte=domain_mapping.note_standard,
                    note_standard_max__gte=domain_mapping.note_standard
                ).first()
                
                domain_data['domain_score'] = {
                    'somme_notes_v': domain_note_v_sum,
                    'note_standard': domain_mapping.note_standard,
                    'rang_percentile': domain_mapping.rang_percentile,
                    'intervalle': intervalle_domaine.intervalle if intervalle_domaine else None,
                    'niveau_adaptatif': niveau_adaptatif.get_niveau_display() if niveau_adaptatif else None
                }
            
            complete_scores.append(domain_data)
    
    return render(request, 'vineland/niveaux_adaptatifs.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': {
            'years': age_years,
            'months': age_months,
            'days': age_days
        }
    })




@login_required
def vineland_age_equivalent(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    scores = calculate_all_scores(questionnaire)
    student = questionnaire.student
    
    # Récupérer les niveaux de confiance
    domain_confidence_levels = {}
    for key, value in request.GET.items():
        if key.startswith('niveau_confiance_'):
            domain_name = key.replace('niveau_confiance_', '')
            domain_confidence_levels[domain_name] = int(value)
    
    # Calcul précis de l'âge avec relativedelta
    age_at_test = relativedelta(questionnaire.created_at.date(), student.date_of_birth)
    print(f"## Age at test: {age_at_test}")
    age_years = age_at_test.years
    print(f"## Age years: {age_years}")
    age_months = age_at_test.months
    print(f"## Age months: {age_months}")
    age_days = age_at_test.days
    print(f"## Age days: {age_days}")
    
    # Déterminer les tranches d'âge
    if age_years < 1:
        return "< 1 an"
    elif age_years == 1:
        tranche_age = '1'
        tranche_age_intervalle = '1'
    elif age_years == 2:
        tranche_age = '2'
        tranche_age_intervalle = '2'
    elif age_years == 3:
        tranche_age = '3'
        tranche_age_intervalle = '3'
    elif age_years == 4:
        tranche_age = '4'
        tranche_age_intervalle = '4'
    elif age_years == 5:
        tranche_age = '5'
        tranche_age_intervalle = '5'
    elif age_years == 6:
        tranche_age = '6'
        tranche_age_intervalle = '6'
    elif 7 <= age_years <= 8:
        tranche_age = '7-8'
        tranche_age_intervalle = '7-8'
    elif 9 <= age_years <= 11:
        tranche_age = '9-11'
        tranche_age_intervalle = '9-11'
    elif 12 <= age_years <= 14:
        tranche_age = '12-14'
        tranche_age_intervalle = '12-14'
    elif 15 <= age_years <= 18:
        tranche_age = '15-18'
        tranche_age_intervalle = '15-18'
    elif 19 <= age_years <= 29:
        tranche_age = '19-29'
        tranche_age_intervalle = '19-29'
    elif 30 <= age_years <= 49:
        tranche_age = '30-49'
        tranche_age_intervalle = '30-49'
    elif age_years >= 50:
        tranche_age = '50-90'
        tranche_age_intervalle = '50-90'


    print(f"## Tranche d'âge: {tranche_age}")
    print(f"## Tranche d'âge intervalle: {tranche_age_intervalle}")


    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            niveau_confiance = domain_confidence_levels.get(domain_name.replace(' ', '_'), 90)
            
            domain_data = {
                'name': domain_name,
                'name_slug': domain_name.replace(' ', '_'),
                'niveau_confiance': niveau_confiance,
                'sous_domaines': [],
                'domain_score': None
            }
            
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )

                echelle_v = None
                for mapping in mappings:
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days))):
                                echelle_v = mapping
                                break
                    else:
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months))):
                                echelle_v = mapping
                                break
                
                query = AgeEquivalentSousDomaine.objects.filter(sous_domaine=sous_domain_obj)

                age_equivalent = query.filter(
                    note_brute_min__lte=score['note_brute']
                ).filter(
                    Q(note_brute_max__isnull=True, note_brute_min=score['note_brute']) |
                    Q(note_brute_max__isnull=False, note_brute_max__gte=score['note_brute'])
                ).first()

                intervalle = IntervaleConfianceSousDomaine.objects.filter(
                    age=tranche_age_intervalle,
                    niveau_confiance=niveau_confiance,
                    sous_domaine=sous_domain_obj
                ).first()
                
                if echelle_v:
                    domain_note_v_sum += echelle_v.note_echelle_v
                    
                    niveau_adaptatif = NiveauAdaptatif.objects.filter(
                        echelle_v_min__lte=echelle_v.note_echelle_v,
                        echelle_v_max__gte=echelle_v.note_echelle_v
                    ).first()
                    
                    domain_data['sous_domaines'].append({
                        'name': sous_domain,
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'intervalle': intervalle.intervalle if intervalle else None,
                        'niveau_adaptatif': niveau_adaptatif.get_niveau_display() if niveau_adaptatif else None,
                        'age_equivalent': age_equivalent.get_age_equivalent_display() if age_equivalent else "-"
                    })
            
            # Debug des données pour NoteDomaineVMapping


            # Recherche du domain_mapping avec une approche plus flexible
            domain_mappings = NoteDomaineVMapping.objects.filter(tranche_age=tranche_age)

            
            domain_mapping = None
            
            if domain_mappings.exists():  # Vérifier qu'il y a des mappings valides
                if 'Communication' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        communication_min__lte=domain_note_v_sum,
                        communication_max__gte=domain_note_v_sum
                    ).first()
                elif 'Vie quotidienne' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        vie_quotidienne_min__lte=domain_note_v_sum,
                        vie_quotidienne_max__gte=domain_note_v_sum
                    ).first()
                elif 'Socialisation' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        socialisation_min__lte=domain_note_v_sum,
                        socialisation_max__gte=domain_note_v_sum
                    ).first()
                elif 'Motricité' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        motricite_min__lte=domain_note_v_sum,
                        motricite_max__gte=domain_note_v_sum
                    ).first()


            intervalle_domaine = IntervaleConfianceDomaine.objects.filter(
                age=tranche_age_intervalle,
                niveau_confiance=niveau_confiance,
                domain__name=domain_name
            ).first()

            # Trouver le niveau adaptatif en utilisant la note standard du domain_mapping
            niveau_adaptatif = None
            if domain_mapping:
                niveau_adaptatif = NiveauAdaptatif.objects.filter(
                    note_standard_min__lte=domain_mapping.note_standard,
                    note_standard_max__gte=domain_mapping.note_standard
                ).first()

            domain_data['domain_score'] = {
                'somme_notes_v': domain_note_v_sum,
                'note_standard': domain_mapping.note_standard if domain_mapping else None,
                'rang_percentile': domain_mapping.rang_percentile if domain_mapping else None,
                'intervalle': intervalle_domaine.intervalle if intervalle_domaine else None,
                'niveau_adaptatif': niveau_adaptatif.get_niveau_display() if niveau_adaptatif else None
            }
            
            complete_scores.append(domain_data)
    
    return render(request, 'vineland/age_equivalent.html', {
        'questionnaire': questionnaire,
        'complete_scores': complete_scores,
        'age': {
            'years': age_years,
            'months': age_months,
            'days': age_days
        }
    })

@login_required
def vineland_comparaisons_paires(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    student = questionnaire.student
    
    # Récupérer le niveau de significativité sélectionné (.05 par défaut)
    niveau_significativite = request.GET.get('niveau_significativite', '.05')
    
    # Calculer l'âge précis avec relativedelta
    age_at_test = relativedelta(questionnaire.created_at.date(), student.date_of_birth)
    age_years = age_at_test.years
    age_months = age_at_test.months
    
    # Déterminer la tranche d'âge pour les tableaux de comparaison
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
    
    # On garde la tranche d'âge simple plus détaillée pour certaines comparaisons
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
    
    # Récupérer les résultats pour ce questionnaire
    scores = calculate_all_scores(questionnaire)
    
    # Préparer les structures pour stocker les comparaisons
    domaine_scores = {}      # Notes standard des domaines
    sous_domaine_scores = {} # Notes échelle-v des sous-domaines
    
    # Récupérer les scores de domaine
    for domain_name, domain_data in scores.items():
        if domain_name != "Comportements problématiques":
            # Calculer la somme des notes-v pour ce domaine
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Recherche du mapping d'échelle-v pour ce sous-domaine et cette note brute
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )
                
                # Trouver le bon mapping d'âge
                echelle_v = None
                for mapping in mappings:
                    # Vérification de l'âge
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_at_test.days))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_at_test.days))):
                                echelle_v = mapping
                                break
                    else:
                        # Vérification sans jours
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months))):
                                echelle_v = mapping
                                break
                
                if echelle_v:
                    sous_domaine_scores[sous_domain] = {
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'domaine': domain_name,
                        'sous_domaine_obj': sous_domain_obj
                    }
                    domain_note_v_sum += echelle_v.note_echelle_v
            
            # Chercher la note standard correspondante pour le domaine
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
                
            domain_mapping = NoteDomaineVMapping.objects.filter(**filter_kwargs).first()
            if domain_mapping:
                domaine_scores[domain_name] = {
                    'note_standard': domain_mapping.note_standard,
                    'domaine_obj': Domain.objects.get(name=domain_name, formulaire_id=questionnaire.formulaire_id),
                    'somme_notes_v': domain_note_v_sum
                }
    
    # Préparation des comparaisons par paires pour les domaines
    domain_comparisons = []
    domaines = list(domaine_scores.keys())
    
    # Générer toutes les paires possibles de domaines
    for i in range(len(domaines)):
        for j in range(i+1, len(domaines)):
            domaine1 = domaines[i]
            domaine2 = domaines[j]
            score1 = domaine_scores[domaine1]['note_standard']
            score2 = domaine_scores[domaine2]['note_standard']
            
            # Chercher les valeurs de signification statistique pour cette paire
            domain1_obj = domaine_scores[domaine1]['domaine_obj']
            domain2_obj = domaine_scores[domaine2]['domaine_obj']
            
            # Calculer la différence absolue entre les scores
            difference = abs(score1 - score2)
            
            # Déterminer le signe correct
            if score1 > score2:
                signe = '>'
            elif score1 < score2:
                signe = '<'
            else:
                signe = '='
            
            # Rechercher la correspondance selon le niveau de significativité sélectionné
            comparison = None
            try:
                comparison = ComparaisonDomaineVineland.objects.get(
                    age=tranche_age_simple,
                    niveau_significativite=niveau_significativite,
                    domaine1=domain1_obj,
                    domaine2=domain2_obj
                )
            except ComparaisonDomaineVineland.DoesNotExist:
                try:
                    comparison = ComparaisonDomaineVineland.objects.get(
                        age=tranche_age_simple,
                        niveau_significativite=niveau_significativite,
                        domaine1=domain2_obj,
                        domaine2=domain1_obj
                    )
                except ComparaisonDomaineVineland.DoesNotExist:
                    comparison = None
            
            # Rechercher les fréquences de différence
            freq = None
            try:
                freq = FrequenceDifferenceDomaineVineland.objects.get(
                    age=tranche_age,
                    domaine1=domain1_obj,
                    domaine2=domain2_obj
                )
            except FrequenceDifferenceDomaineVineland.DoesNotExist:
                try:
                    freq = FrequenceDifferenceDomaineVineland.objects.get(
                        age=tranche_age,
                        domaine1=domain2_obj,
                        domaine2=domain1_obj
                    )
                except FrequenceDifferenceDomaineVineland.DoesNotExist:
                    freq = None
            
            # Déterminer si la différence est significative
            est_significatif = comparison and difference >= comparison.difference_requise
            
            # Déterminer la fréquence de la différence
            frequence = None
            if freq:
                # Fonction pour extraire la partie numérique
                def extract_number(value):
                    if not value:
                        return 9999  # Valeur très élevée par défaut
                    # Si la valeur se termine par +, prendre juste la partie numérique
                    if value.endswith('+'):
                        return int(value[:-1])
                    # Si c'est un intervalle comme "20-23", prendre la valeur minimale
                    elif '-' in value:
                        return int(value.split('-')[0])
                    # Sinon, essayer de convertir directement
                    else:
                        try:
                            return int(value)
                        except ValueError:
                            return 9999  # En cas d'erreur, retourner une valeur très élevée
                
                # Comparer la différence avec les seuils de fréquence
                if freq.frequence_5 and difference >= extract_number(freq.frequence_5):
                    frequence = "5%"
                elif freq.frequence_10 and difference >= extract_number(freq.frequence_10):
                    frequence = "10%"
                elif freq.frequence_16 and difference >= extract_number(freq.frequence_16):
                    frequence = "16%"
            
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
    
    # Préparation des comparaisons par paires pour les sous-domaines, groupées par domaine
    sous_domaine_grouped = {}
    for sous_domaine, data in sous_domaine_scores.items():
        domaine = data['domaine']
        if domaine not in sous_domaine_grouped:
            sous_domaine_grouped[domaine] = []
        sous_domaine_grouped[domaine].append(sous_domaine)
    
    sous_domaine_comparisons = {}
    for domaine, sous_domaines in sous_domaine_grouped.items():
        sous_domaine_comparisons[domaine] = []
        
        # Générer toutes les paires possibles de sous-domaines pour ce domaine
        for i in range(len(sous_domaines)):
            for j in range(i+1, len(sous_domaines)):
                sous_domaine1 = sous_domaines[i]
                sous_domaine2 = sous_domaines[j]
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                # Calculer la différence absolue entre les scores
                difference = abs(note1 - note2)
                
                # Déterminer le signe correct
                if note1 > note2:
                    signe = '>'
                elif note1 < note2:
                    signe = '<'
                else:
                    signe = '='
                
                # Rechercher la correspondance selon le niveau de significativité sélectionné
                comparison = None
                try:
                    # Utiliser la nouvelle table ComparaisonSousDomaineVineland
                    comparison = ComparaisonSousDomaineVineland.objects.get(
                        age=tranche_age,  # Utiliser la tranche d'âge standard
                        niveau_significativite=niveau_significativite,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except ComparaisonSousDomaineVineland.DoesNotExist:
                    try:
                        # Essayer dans l'autre sens car les comparaisons sont symétriques
                        comparison = ComparaisonSousDomaineVineland.objects.get(
                            age=tranche_age,  # Utiliser la tranche d'âge standard
                            niveau_significativite=niveau_significativite,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except ComparaisonSousDomaineVineland.DoesNotExist:
                        comparison = None
                
                # Déterminer si la différence est significative
                est_significatif = comparison and difference >= comparison.difference_requise
                
                # AJOUT: Rechercher les fréquences de différence pour les sous-domaines
                freq = None
                try:
                    freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                        age=tranche_age,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                    try:
                        freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                            age=tranche_age,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                        freq = None
                
                # AJOUT: Déterminer la fréquence de la différence
                frequence = None
                if freq:
                    # Fonction pour extraire la partie numérique
                    def extract_number(value):
                        if not value:
                            return 9999  # Valeur très élevée par défaut
                        # Si la valeur se termine par +, prendre juste la partie numérique
                        if value.endswith('+'):
                            return int(value[:-1])
                        # Si c'est un intervalle comme "20-23", prendre la valeur minimale
                        elif '-' in value:
                            return int(value.split('-')[0])
                        # Sinon, essayer de convertir directement
                        else:
                            try:
                                return int(value)
                            except ValueError:
                                return 9999  # En cas d'erreur, retourner une valeur très élevée
                    
                    # Comparer la différence avec les seuils de fréquence
                    if freq.frequence_5 and difference >= extract_number(freq.frequence_5):
                        frequence = "5%"
                    elif freq.frequence_10 and difference >= extract_number(freq.frequence_10):
                        frequence = "10%"
                    elif freq.frequence_16 and difference >= extract_number(freq.frequence_16):
                        frequence = "16%"
                
                sous_domaine_comparisons[domaine].append({
                    'sous_domaine1': sous_domaine1,
                    'sous_domaine2': sous_domaine2,
                    'note1': note1,
                    'note2': note2,
                    'signe': signe,
                    'difference': difference,
                    'difference_requise': comparison.difference_requise if comparison else None,
                    'est_significatif': est_significatif,
                    'frequence': frequence  # MODIFIÉ: Ajout de la fréquence pour les sous-domaines
                })
    
    # NOUVELLE SECTION: Préparation des comparaisons inter-domaines pour les sous-domaines
    interdomaine_comparisons = []
    all_sous_domaines = list(sous_domaine_scores.keys())
    
    # Générer toutes les paires possibles de sous-domaines appartenant à des domaines différents
    for i in range(len(all_sous_domaines)):
        for j in range(i+1, len(all_sous_domaines)):
            sous_domaine1 = all_sous_domaines[i]
            sous_domaine2 = all_sous_domaines[j]
            
            # Vérifier que les sous-domaines appartiennent à des domaines différents
            domaine1 = sous_domaine_scores[sous_domaine1]['domaine']
            domaine2 = sous_domaine_scores[sous_domaine2]['domaine']
            
            if domaine1 != domaine2:  # Seulement si domaines différents
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                # Calculer la différence absolue entre les scores
                difference = abs(note1 - note2)
                
                # Déterminer le signe correct
                if note1 > note2:
                    signe = '>'
                elif note1 < note2:
                    signe = '<'
                else:
                    signe = '='
                
                # Rechercher la correspondance selon le niveau de significativité sélectionné
                comparison = None
                try:
                    comparison = ComparaisonSousDomaineVineland.objects.get(
                        age=tranche_age,
                        niveau_significativite=niveau_significativite,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except ComparaisonSousDomaineVineland.DoesNotExist:
                    try:
                        comparison = ComparaisonSousDomaineVineland.objects.get(
                            age=tranche_age,
                            niveau_significativite=niveau_significativite,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except ComparaisonSousDomaineVineland.DoesNotExist:
                        comparison = None
                
                # Déterminer si la différence est significative
                est_significatif = comparison and difference >= comparison.difference_requise
                
                # Rechercher les fréquences de différence
                freq = None
                try:
                    freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                        age=tranche_age,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                    try:
                        freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                            age=tranche_age,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                        freq = None
                
                # Déterminer la fréquence de la différence
                frequence = None
                if freq:
                    # Réutiliser la fonction extract_number définie plus haut
                    def extract_number(value):
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
                    
                    # Comparer la différence avec les seuils de fréquence
                    if freq.frequence_5 and difference >= extract_number(freq.frequence_5):
                        frequence = "5%"
                    elif freq.frequence_10 and difference >= extract_number(freq.frequence_10):
                        frequence = "10%"
                    elif freq.frequence_16 and difference >= extract_number(freq.frequence_16):
                        frequence = "16%"
                
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
    
    # Sélection de comparaisons - préparation pour l'éventuelle sélection manuelle
    selection_comparisons = []
    
    return render(request, 'vineland/comparaisons_paires.html', {
        'questionnaire': questionnaire,
        'niveau_significativite': niveau_significativite,
        'tranche_age': tranche_age,
        'age': {
            'years': age_years,
            'months': age_months,
            'days': age_at_test.days
        },
        'domain_comparisons': domain_comparisons,
        'sous_domaine_comparisons': sous_domaine_comparisons,
        'interdomaine_comparisons': interdomaine_comparisons,  # Ajout des comparaisons inter-domaines
        'selection_comparisons': selection_comparisons
    })

##############################################################################################################################################################################
@login_required
def import_comparaison_sous_domaine_data(request):
    """Vue pour importer les données de comparaison des sous-domaines Vineland"""
    from django.db import transaction
    import json
    
    # Structure par tranche d'âge
    age_ranges = ["1-2", "3-6", "7-18", "19-49", "50-90"]
    
    # Liste des sous-domaines dans l'ordre du tableau
    sous_domaines = [
        "Réceptive", "Expressive", "Écrite", "Personnelle", "Domestique", 
        "Communautaire", "Relations interpersonnelles", "Jeu et temps libre", 
        "Adaptation", "Globale", "Fine"
    ]
    
    # Valeurs initiales - placez votre JSON ici
    initial_values = {}
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        # Vérifier si des données modifiées ont été soumises
        if 'modified_data' in request.POST and request.POST['modified_data']:
            try:
                # Utiliser les données modifiées par l'utilisateur
                data = json.loads(request.POST['modified_data'])
            except json.JSONDecodeError:
                error_message = "Erreur: Le format JSON n'est pas valide."
                data = initial_values
        else:
            # Utiliser les données initiales
            data = initial_values
        
        # Récupération des sous-domaines
        sous_domaines_objects = {}
        for sd_name in sous_domaines:
            sd = SousDomain.objects.filter(name=sd_name).first()
            if sd:
                sous_domaines_objects[sd_name] = sd
            else:
                # Essayer avec un nom similaire
                for d in SousDomain.objects.all():
                    if sd_name.lower() in d.name.lower():
                        sous_domaines_objects[sd_name] = d
                        break
        
        # Vérification que tous les sous-domaines sont trouvés
        missing_sous_domaines = [name for name in sous_domaines if name not in sous_domaines_objects]
        
        if missing_sous_domaines:
            error_message = f"Sous-domaines manquants: {', '.join(missing_sous_domaines)}"
            # Afficher les sous-domaines trouvés pour aider au débogage
            error_message += f"\nSous-domaines trouvés: {', '.join([f'{k}: {v.name}' for k, v in sous_domaines_objects.items()])}"
        else:
            # Import des données
            created_count = 0
            error_count = 0
            skipped_count = 0
            
            # Utiliser une transaction pour tout importer en une seule opération
            with transaction.atomic():
                # Supprimer les anciennes données
                ComparaisonSousDomaineVineland.objects.all().delete()
                
                for age in age_ranges:
                    if age in data:
                        for sd1_name, sd1_data in data[age].items():
                            for sd2_name, values in sd1_data.items():
                                # Vérifier si cette paire a des valeurs
                                has_values = False
                                if values.get('05') is not None or values.get('01') is not None:
                                    has_values = True
                                
                                if has_values:
                                    sd1 = sous_domaines_objects.get(sd1_name)
                                    sd2 = sous_domaines_objects.get(sd2_name)
                                    
                                    if not sd1 or not sd2:
                                        error_count += 1
                                        continue
                                    
                                    # Traiter les valeurs de significativité .05
                                    if values.get('05') is not None:
                                        try:
                                            ComparaisonSousDomaineVineland.objects.create(
                                                age=age,
                                                niveau_significativite='.05',
                                                sous_domaine1=sd1,
                                                sous_domaine2=sd2,
                                                difference_requise=values['05']
                                            )
                                            created_count += 1
                                        except Exception as e:
                                            error_count += 1
                                            print(f"Erreur pour {age}, {sd1_name}/{sd2_name} (.05): {str(e)}")
                                    
                                    # Traiter les valeurs de significativité .01
                                    if values.get('01') is not None:
                                        try:
                                            ComparaisonSousDomaineVineland.objects.create(
                                                age=age,
                                                niveau_significativite='.01',
                                                sous_domaine1=sd1,
                                                sous_domaine2=sd2,
                                                difference_requise=values['01']
                                            )
                                            created_count += 1
                                        except Exception as e:
                                            error_count += 1
                                            print(f"Erreur pour {age}, {sd1_name}/{sd2_name} (.01): {str(e)}")
                                else:
                                    skipped_count += 1
            
            success_message = f"{created_count} comparaisons importées avec succès, {error_count} erreurs, {skipped_count} ignorées"
    
    # Compte le nombre d'enregistrements déjà existants
    existing_count = ComparaisonSousDomaineVineland.objects.count()
    
    # Préparer le contexte
    context = {
        'age_ranges': age_ranges,
        'sous_domaines': sous_domaines,
        'values': initial_values,
        'existing_count': existing_count
    }
    
    if existing_count > 0:
        context['info'] = f"Il y a déjà {existing_count} comparaisons dans la base de données. Cliquer sur 'Importer' pour remplacer ces données."
    
    if error_message:
        context['error'] = error_message
    if success_message:
        context['success'] = success_message
    
    return render(request, 'vineland/import_comparaison_sous_domaine_data.html', context)

import io
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from polls.models import Questionnaire, Student
from .models import EchelleVMapping, NoteDomaineVMapping, NiveauAdaptatif, AgeEquivalentSousDomaine
from .models import ComparaisonDomaineVineland, ComparaisonSousDomaineVineland
from .models import FrequenceDifferenceDomaineVineland, FrequenceDifferenceSousDomaineVineland
from .utils.scoring import calculate_all_scores
from django.db.models import Q
from dateutil.relativedelta import relativedelta

@login_required
def vineland_export_pdf(request, questionnaire_id):
    # Récupérer le questionnaire et les données de base
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    student = questionnaire.student
    reponses = ReponseVineland.objects.filter(questionnaire=questionnaire).select_related('question')
    
    # Vérifier la structure du modèle QuestionVineland
    if reponses.exists():
        first_question = reponses.first().question
        # Vérifier les attributs disponibles
        question_attrs = dir(first_question)
        # Déterminer quel attribut utiliser pour le texte de la question
        text_attr_options = ['libelle', 'text', 'texte', 'question_text']
        for attr in text_attr_options:
            if attr in question_attrs:
                question_text_attr = attr
                break
        else:
            question_text_attr = None
        
        # Déterminer quel attribut utiliser pour le numéro de l'item
        num_attr_options = ['numero_item', 'num_question', 'numero', 'id']
        for attr in num_attr_options:
            if attr in question_attrs:
                question_num_attr = attr
                break
        else:
            question_num_attr = None
    else:
        # Valeurs par défaut si aucune réponse n'existe
        question_text_attr = None
        question_num_attr = None
    
    # Calculer l'âge précis avec relativedelta
    age_at_test = relativedelta(questionnaire.created_at.date(), student.date_of_birth)
    age_years = age_at_test.years
    age_months = age_at_test.months
    age_days = age_at_test.days
    
    # Déterminer la tranche d'âge
    if age_years < 3:
        tranche_age = '1-2'
        tranche_age_simple = '1' if age_years < 2 else '2'
    elif age_years < 7:
        tranche_age = '3-6'
        tranche_age_simple = str(age_years)
    elif age_years < 9:
        tranche_age = '7-18'
        tranche_age_simple = '7-8'
    elif age_years < 12:
        tranche_age = '7-18'
        tranche_age_simple = '9-11'
    elif age_years < 15:
        tranche_age = '7-18'
        tranche_age_simple = '12-14'
    elif age_years < 19:
        tranche_age = '7-18'
        tranche_age_simple = '15-18'
    elif age_years < 30:
        tranche_age = '19-29'
        tranche_age_simple = '19-29'
    elif age_years < 50:
        tranche_age = '30-49'
        tranche_age_simple = '30-49'
    else:
        tranche_age = '50-90'
        tranche_age_simple = '50-90'
    
    # Préparation du PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vineland_rapport_{student.name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Liste pour stocker tous les éléments du document
    elements = []
    
    # --- PAGE 1: Page de couverture ---
    elements.append(Paragraph(f"Rapport d'évaluation Vineland-II", title_style))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"Enfant: {student.name}", subtitle_style))
    elements.append(Paragraph(f"Date de naissance: {student.date_of_birth.strftime('%d/%m/%Y')}", normal_style))
    elements.append(Paragraph(f"Âge au moment du test: {age_years} ans, {age_months} mois, {age_days} jours", normal_style))
    elements.append(Paragraph(f"Date d'évaluation: {questionnaire.created_at.strftime('%d/%m/%Y')}", normal_style))
    elements.append(Paragraph(f"Évaluateur: {questionnaire.parent.get_full_name() or questionnaire.parent.username}", normal_style))
    elements.append(PageBreak())
    
    # --- PAGE 2: Questions et réponses ---
    elements.append(Paragraph("Questions et Réponses", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Regrouper les réponses par domaine et sous-domaine
    grouped_responses = {}
    for reponse in reponses:
        domaine = reponse.question.sous_domaine.domain.name
        sous_domaine = reponse.question.sous_domaine.name
        
        if domaine not in grouped_responses:
            grouped_responses[domaine] = {}
            
        if sous_domaine not in grouped_responses[domaine]:
            grouped_responses[domaine][sous_domaine] = []
            
        grouped_responses[domaine][sous_domaine].append(reponse)
    
    # Créer des tableaux pour chaque domaine
    for domaine, sous_domaines in grouped_responses.items():
        elements.append(Paragraph(f"Domaine: {domaine}", subtitle_style))
    
        for sous_domaine, responses in sous_domaines.items():
            elements.append(Paragraph(f"Sous-domaine: {sous_domaine}", styles["Heading3"]))
            
            # Créer un style spécifique avec un nom unique pour éviter les conflits
            question_style = ParagraphStyle(
                name=f'QuestionStyle_{domaine}_{sous_domaine}',  # Nom unique
                fontName='Helvetica',
                fontSize=9,
                leading=11,
                wordWrap='CJK',  # Améliore le retour à la ligne
                alignment=0  # 0 = left aligned
            )
            
            # Tableau des questions/réponses
            data = []
            data.append([Paragraph("<b>Item</b>", styles["Normal"]), 
                            Paragraph("<b>Question</b>", styles["Normal"]), 
                            Paragraph("<b>Réponse</b>", styles["Normal"])])
            
            for idx, reponse in enumerate(responses):
                # Récupérer le texte de la question et le numéro de manière sécurisée
                try:
                    question_text = getattr(reponse.question, question_text_attr, f"Question {idx+1}")
                except (AttributeError, TypeError):
                    question_text = f"Question {idx+1}"
                
                try:
                    question_num = getattr(reponse.question, question_num_attr, idx+1)
                except (AttributeError, TypeError):
                    question_num = idx+1
                
                # Créer des paragraphes pour chaque cellule
                item_para = Paragraph(str(question_num), styles["Normal"])
                # Utiliser le style spécifique pour la question
                question_para = Paragraph(question_text, question_style)
                reponse_para = Paragraph(reponse.reponse, styles["Normal"])
                
                data.append([item_para, question_para, reponse_para])
            
            # Créer le tableau avec des largeurs fixes
            table = Table(data, colWidths=[1*cm, 13*cm, 2*cm], repeatRows=1)
            
            # Style de tableau avec des ajustements pour les questions longues
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('TOPPADDING', (0, 0), (-1, 0), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),  # Plus d'espace en bas
                ('TOPPADDING', (0, 1), (-1, -1), 6),     # Plus d'espace en haut
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),     # Alignement en haut important
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),    # Centrer les numéros
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),    # Centrer les réponses
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 0.5*cm))
        
        elements.append(Spacer(1, 0.5*cm))
    
    elements.append(PageBreak())
    
    # --- PAGE 3: Synthèse des scores ---
    elements.append(Paragraph("Synthèse des Résultats", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Récupérer tous les scores calculés
    scores = calculate_all_scores(questionnaire)
    
    # Calculer les scores de domaine et les niveaux adaptatifs
    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            domain_data = {
                'name': domain_name,
                'sous_domaines': [],
                'domain_score': None
            }
            
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Recherche des mappings correspondant à la note brute
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )

                # Recherche de la correspondance d'âge
                echelle_v = None
                for mapping in mappings:
                    # Vérification avec jours si présents
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        if ((mapping.age_debut_annee < age_years) or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days)):
                            if ((mapping.age_fin_annee > age_years) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days)):
                                echelle_v = mapping
                                break
                    else:
                        # Vérification sans jours
                        if ((mapping.age_debut_annee < age_years) or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months)):
                            if ((mapping.age_fin_annee > age_years) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months)):
                                echelle_v = mapping
                                break
                
                # Recherche de l'âge équivalent
                age_equivalent = AgeEquivalentSousDomaine.objects.filter(
                    sous_domaine=sous_domain_obj
                ).filter(
                    note_brute_min__lte=score['note_brute']
                ).filter(
                    Q(note_brute_max__isnull=True, note_brute_min=score['note_brute']) |
                    Q(note_brute_max__isnull=False, note_brute_max__gte=score['note_brute'])
                ).first()
                
                if echelle_v:
                    domain_note_v_sum += echelle_v.note_echelle_v
                    
                    # Trouver le niveau adaptatif
                    niveau_adaptatif = NiveauAdaptatif.objects.filter(
                        echelle_v_min__lte=echelle_v.note_echelle_v,
                        echelle_v_max__gte=echelle_v.note_echelle_v
                    ).first()
                    
                    domain_data['sous_domaines'].append({
                        'name': sous_domain,
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'niveau_adaptatif': niveau_adaptatif.get_niveau_display() if niveau_adaptatif else "Non disponible",
                        'age_equivalent': age_equivalent.get_age_equivalent_display() if age_equivalent else "Non disponible"
                    })
            
            # Recherche du domain_mapping
            domain_mappings = NoteDomaineVMapping.objects.filter(tranche_age=tranche_age)
            domain_mapping = None
            
            if domain_mappings.exists():
                if 'Communication' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        communication_min__lte=domain_note_v_sum,
                        communication_max__gte=domain_note_v_sum
                    ).first()
                elif 'Vie quotidienne' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        vie_quotidienne_min__lte=domain_note_v_sum,
                        vie_quotidienne_max__gte=domain_note_v_sum
                    ).first()
                elif 'Socialisation' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        socialisation_min__lte=domain_note_v_sum,
                        socialisation_max__gte=domain_note_v_sum
                    ).first()
                elif 'Motricité' in domain_name:
                    domain_mapping = domain_mappings.filter(
                        motricite_min__lte=domain_note_v_sum,
                        motricite_max__gte=domain_note_v_sum
                    ).first()
            
            # Trouver le niveau adaptatif du domaine
            niveau_adaptatif_domain = None
            if domain_mapping:
                niveau_adaptatif_domain = NiveauAdaptatif.objects.filter(
                    note_standard_min__lte=domain_mapping.note_standard,
                    note_standard_max__gte=domain_mapping.note_standard
                ).first()
            
            domain_data['domain_score'] = {
                'somme_notes_v': domain_note_v_sum,
                'note_standard': domain_mapping.note_standard if domain_mapping else None,
                'rang_percentile': domain_mapping.rang_percentile if domain_mapping else None,
                'niveau_adaptatif': niveau_adaptatif_domain.get_niveau_display() if niveau_adaptatif_domain else "Non disponible"
            }
            
            complete_scores.append(domain_data)
    
    # Générer la synthèse des scores
    for domain in complete_scores:
        elements.append(Paragraph(f"Domaine: {domain['name']}", subtitle_style))
        
        # Tableau du score de domaine
        if domain['domain_score']:
            domain_score_data = [
                ["Somme des notes-V", "Note standard", "Rang percentile", "Niveau adaptatif"],
                [
                    str(domain['domain_score']['somme_notes_v']),
                    str(domain['domain_score']['note_standard'] or "-"),
                    str(domain['domain_score']['rang_percentile'] or "-"),
                    domain['domain_score']['niveau_adaptatif']
                ]
            ]
            
            domain_table = Table(domain_score_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
            domain_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ]))
            
            elements.append(domain_table)
            elements.append(Spacer(1, 0.5*cm))
        
        # Tableau des sous-domaines
        sous_domaine_data = [["Sous-domaine", "Note brute", "Note échelle-V", "Niveau adaptatif", "Âge équivalent"]]
        
        for sous_domain in domain['sous_domaines']:
            sous_domaine_data.append([
                sous_domain['name'],
                str(sous_domain['note_brute']),
                str(sous_domain['note_echelle_v']),
                sous_domain['niveau_adaptatif'],
                sous_domain['age_equivalent']
            ])
        
        sous_domaine_table = Table(sous_domaine_data, colWidths=[5*cm, 2.5*cm, 2.5*cm, 4*cm, 3*cm])
        sous_domaine_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (1, 1), (2, -1), 'CENTER'),
        ]))
        
        elements.append(sous_domaine_table)
        elements.append(Spacer(1, 1*cm))
    
    elements.append(PageBreak())
    
    # --- PAGE 4: Comparaisons par paires ---
    elements.append(Paragraph("Comparaisons par paires", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Préparer les structures pour stocker les comparaisons
    domaine_scores = {}      # Notes standard des domaines
    sous_domaine_scores = {} # Notes échelle-v des sous-domaines
    
    # Récupérer les scores de domaine
    for domain_name, domain_data in scores.items():
        if domain_name != "Comportements problématiques":
            # Calculer la somme des notes-v pour ce domaine
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Recherche du mapping d'échelle-v pour ce sous-domaine et cette note brute
                mappings = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                )
                
                # Trouver le bon mapping d'âge
                echelle_v = None
                for mapping in mappings:
                    # Vérification de l'âge
                    if mapping.age_debut_jour is not None and mapping.age_fin_jour is not None:
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months) or
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois == age_months and mapping.age_debut_jour <= age_days))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months) or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois == age_months and mapping.age_fin_jour >= age_days))):
                                echelle_v = mapping
                                break
                    else:
                        # Vérification sans jours
                        if ((mapping.age_debut_annee < age_years or 
                            (mapping.age_debut_annee == age_years and mapping.age_debut_mois <= age_months))):
                            if ((mapping.age_fin_annee > age_years or
                                (mapping.age_fin_annee == age_years and mapping.age_fin_mois >= age_months))):
                                echelle_v = mapping
                                break
                
                if echelle_v:
                    sous_domaine_scores[sous_domain] = {
                        'note_echelle_v': echelle_v.note_echelle_v,
                        'domaine': domain_name,
                        'sous_domaine_obj': sous_domain_obj
                    }
                    domain_note_v_sum += echelle_v.note_echelle_v
            
            # Chercher la note standard correspondante pour le domaine
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
                
            domain_mapping = NoteDomaineVMapping.objects.filter(**filter_kwargs).first()
            if domain_mapping:
                domaine_scores[domain_name] = {
                    'note_standard': domain_mapping.note_standard,
                    'domaine_obj': Domain.objects.get(name=domain_name, formulaire_id=questionnaire.formulaire_id),
                    'somme_notes_v': domain_note_v_sum
                }
    
    # Niveau de significativité
    niveau_significativite = ".05"  # Valeur par défaut
    
    # Préparation des comparaisons par paires pour les domaines
    domain_comparisons = []
    domaines = list(domaine_scores.keys())
    
    # Générer toutes les paires possibles de domaines
    for i in range(len(domaines)):
        for j in range(i+1, len(domaines)):
            domaine1 = domaines[i]
            domaine2 = domaines[j]
            score1 = domaine_scores[domaine1]['note_standard']
            score2 = domaine_scores[domaine2]['note_standard']
            
            # Chercher les valeurs de signification statistique pour cette paire
            domain1_obj = domaine_scores[domaine1]['domaine_obj']
            domain2_obj = domaine_scores[domaine2]['domaine_obj']
            
            # Calculer la différence absolue entre les scores
            difference = abs(score1 - score2)
            
            # Déterminer le signe correct
            if score1 > score2:
                signe = '>'
            elif score1 < score2:
                signe = '<'
            else:
                signe = '='
            
            # Rechercher la correspondance selon le niveau de significativité sélectionné
            comparison = None
            try:
                comparison = ComparaisonDomaineVineland.objects.get(
                    age=tranche_age_simple,
                    niveau_significativite=niveau_significativite,
                    domaine1=domain1_obj,
                    domaine2=domain2_obj
                )
            except ComparaisonDomaineVineland.DoesNotExist:
                try:
                    comparison = ComparaisonDomaineVineland.objects.get(
                        age=tranche_age_simple,
                        niveau_significativite=niveau_significativite,
                        domaine1=domain2_obj,
                        domaine2=domain1_obj
                    )
                except ComparaisonDomaineVineland.DoesNotExist:
                    comparison = None
            
            # Rechercher les fréquences de différence
            freq = None
            try:
                freq = FrequenceDifferenceDomaineVineland.objects.get(
                    age=tranche_age,
                    domaine1=domain1_obj,
                    domaine2=domain2_obj
                )
            except FrequenceDifferenceDomaineVineland.DoesNotExist:
                try:
                    freq = FrequenceDifferenceDomaineVineland.objects.get(
                        age=tranche_age,
                        domaine1=domain2_obj,
                        domaine2=domain1_obj
                    )
                except FrequenceDifferenceDomaineVineland.DoesNotExist:
                    freq = None
            
            # Déterminer si la différence est significative
            est_significatif = comparison and difference >= comparison.difference_requise
            
            # Fonction interne pour extraire le nombre d'une chaîne
            def extract_number(value):
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
            
            # Déterminer la fréquence de la différence
            frequence = None
            if freq:
                if freq.frequence_5 and difference >= extract_number(freq.frequence_5):
                    frequence = "5%"
                elif freq.frequence_10 and difference >= extract_number(freq.frequence_10):
                    frequence = "10%"
                elif freq.frequence_16 and difference >= extract_number(freq.frequence_16):
                    frequence = "16%"
            
            domain_comparisons.append({
                'domaine1': domaine1,
                'domaine2': domaine2,
                'note1': score1,
                'note2': score2,
                'signe': signe,
                'difference': difference,
                'est_significatif': est_significatif,
                'frequence': frequence
            })
    
    # Afficher le tableau des comparaisons de domaines
    if domain_comparisons:
        elements.append(Paragraph("Comparaisons des domaines", subtitle_style))
        
        domain_comparison_data = [["Domaine 1", "Note", "<, >, ou =", "Note", "Domaine 2", "Différence", "Significatif", "Fréquence"]]
        
        for comparison in domain_comparisons:
            domain_comparison_data.append([
                comparison['domaine1'],
                str(comparison['note1']),
                comparison['signe'],
                str(comparison['note2']),
                comparison['domaine2'],
                str(comparison['difference']),
                "✓" if comparison['est_significatif'] else "-",
                comparison['frequence'] if comparison['frequence'] else "-"
            ])
        
        domain_comparison_table = Table(domain_comparison_data, colWidths=[3*cm, 1.5*cm, 1.5*cm, 1.5*cm, 3*cm, 2*cm, 2*cm, 2*cm])
        domain_comparison_table.setStyle(TableStyle([
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
        ]))
        
        elements.append(domain_comparison_table)
        elements.append(Spacer(1, 1*cm))
    
    # Préparation des comparaisons par paires pour les sous-domaines, groupées par domaine
    sous_domaine_grouped = {}
    for sous_domaine, data in sous_domaine_scores.items():
        domaine = data['domaine']
        if domaine not in sous_domaine_grouped:
            sous_domaine_grouped[domaine] = []
        sous_domaine_grouped[domaine].append(sous_domaine)
    
    sous_domaine_comparisons = {}
    for domaine, sous_domaines in sous_domaine_grouped.items():
        sous_domaine_comparisons[domaine] = []
        
        # Générer toutes les paires possibles de sous-domaines pour ce domaine
        for i in range(len(sous_domaines)):
            for j in range(i+1, len(sous_domaines)):
                sous_domaine1 = sous_domaines[i]
                sous_domaine2 = sous_domaines[j]
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                # Calculer la différence absolue entre les scores
                difference = abs(note1 - note2)
                
                # Déterminer le signe correct
                if note1 > note2:
                    signe = '>'
                elif note1 < note2:
                    signe = '<'
                else:
                    signe = '='
                
                # Rechercher la correspondance selon le niveau de significativité sélectionné
                comparison = None
                try:
                    comparison = ComparaisonSousDomaineVineland.objects.get(
                        age=tranche_age,
                        niveau_significativite=niveau_significativite,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except ComparaisonSousDomaineVineland.DoesNotExist:
                    try:
                        comparison = ComparaisonSousDomaineVineland.objects.get(
                            age=tranche_age,
                            niveau_significativite=niveau_significativite,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except ComparaisonSousDomaineVineland.DoesNotExist:
                        comparison = None
                
                # Déterminer si la différence est significative
                est_significatif = comparison and difference >= comparison.difference_requise
                
                # Rechercher les fréquences de différence
                freq = None
                try:
                    freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                        age=tranche_age,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                    try:
                        freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                            age=tranche_age,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                        freq = None
                
                # Déterminer la fréquence de la différence
                frequence = None
                if freq:
                    # Réutiliser la fonction extract_number définie plus haut
                    if freq.frequence_5 and difference >= extract_number(freq.frequence_5):
                        frequence = "5%"
                    elif freq.frequence_10 and difference >= extract_number(freq.frequence_10):
                        frequence = "10%"
                    elif freq.frequence_16 and difference >= extract_number(freq.frequence_16):
                        frequence = "16%"
                
                sous_domaine_comparisons[domaine].append({
                    'sous_domaine1': sous_domaine1,
                    'sous_domaine2': sous_domaine2,
                    'note1': note1,
                    'note2': note2,
                    'signe': signe,
                    'difference': difference,
                    'est_significatif': est_significatif,
                    'frequence': frequence
                })
    
    # Afficher les comparaisons de sous-domaines par domaine
    for domaine, comparisons in sous_domaine_comparisons.items():
        if comparisons:
            elements.append(Paragraph(f"Comparaisons des sous-domaines - {domaine}", subtitle_style))
            
            sous_domaine_comparison_data = [["Sous-domaine 1", "Note", "<, >, ou =", "Note", "Sous-domaine 2", "Différence", "Significatif", "Fréquence"]]
            
            for comparison in comparisons:
                sous_domaine_comparison_data.append([
                    comparison['sous_domaine1'],
                    str(comparison['note1']),
                    comparison['signe'],
                    str(comparison['note2']),
                    comparison['sous_domaine2'],
                    str(comparison['difference']),
                    "✓" if comparison['est_significatif'] else "-",
                    comparison['frequence'] if comparison['frequence'] else "-"
                ])
            
            sous_domaine_comparison_table = Table(sous_domaine_comparison_data, colWidths=[3*cm, 1.5*cm, 1.5*cm, 1.5*cm, 3*cm, 2*cm, 2*cm, 2*cm])
            sous_domaine_comparison_table.setStyle(TableStyle([
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
            ]))
            
            elements.append(sous_domaine_comparison_table)
            elements.append(Spacer(1, 1*cm))
    
    # Préparation des comparaisons inter-domaines pour les sous-domaines
    interdomaine_comparisons = []
    all_sous_domaines = list(sous_domaine_scores.keys())
    
    # Générer toutes les paires possibles de sous-domaines appartenant à des domaines différents
    for i in range(len(all_sous_domaines)):
        for j in range(i+1, len(all_sous_domaines)):
            sous_domaine1 = all_sous_domaines[i]
            sous_domaine2 = all_sous_domaines[j]
            
            # Vérifier que les sous-domaines appartiennent à des domaines différents
            domaine1 = sous_domaine_scores[sous_domaine1]['domaine']
            domaine2 = sous_domaine_scores[sous_domaine2]['domaine']
            
            if domaine1 != domaine2:  # Seulement si domaines différents
                note1 = sous_domaine_scores[sous_domaine1]['note_echelle_v']
                note2 = sous_domaine_scores[sous_domaine2]['note_echelle_v']
                
                sous_domaine1_obj = sous_domaine_scores[sous_domaine1]['sous_domaine_obj']
                sous_domaine2_obj = sous_domaine_scores[sous_domaine2]['sous_domaine_obj']
                
                # Calculer la différence absolue entre les scores
                difference = abs(note1 - note2)
                
                # Déterminer le signe correct
                if note1 > note2:
                    signe = '>'
                elif note1 < note2:
                    signe = '<'
                else:
                    signe = '='
                
                # Rechercher la correspondance selon le niveau de significativité sélectionné
                comparison = None
                try:
                    comparison = ComparaisonSousDomaineVineland.objects.get(
                        age=tranche_age,
                        niveau_significativite=niveau_significativite,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except ComparaisonSousDomaineVineland.DoesNotExist:
                    try:
                        comparison = ComparaisonSousDomaineVineland.objects.get(
                            age=tranche_age,
                            niveau_significativite=niveau_significativite,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except ComparaisonSousDomaineVineland.DoesNotExist:
                        comparison = None
                
                # Déterminer si la différence est significative
                est_significatif = comparison and difference >= comparison.difference_requise
                
                # Rechercher les fréquences de différence
                freq = None
                try:
                    freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                        age=tranche_age,
                        sous_domaine1=sous_domaine1_obj,
                        sous_domaine2=sous_domaine2_obj
                    )
                except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                    try:
                        freq = FrequenceDifferenceSousDomaineVineland.objects.get(
                            age=tranche_age,
                            sous_domaine1=sous_domaine2_obj,
                            sous_domaine2=sous_domaine1_obj
                        )
                    except FrequenceDifferenceSousDomaineVineland.DoesNotExist:
                        freq = None
                
                # Déterminer la fréquence de la différence
                frequence = None
                if freq:
                    # Réutiliser la fonction extract_number définie plus haut
                    if freq.frequence_5 and difference >= extract_number(freq.frequence_5):
                        frequence = "5%"
                    elif freq.frequence_10 and difference >= extract_number(freq.frequence_10):
                        frequence = "10%"
                    elif freq.frequence_16 and difference >= extract_number(freq.frequence_16):
                        frequence = "16%"
                
                interdomaine_comparisons.append({
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
    
    # Afficher le tableau des comparaisons inter-domaines
    # Afficher le tableau des comparaisons inter-domaines
    if interdomaine_comparisons:
        elements.append(Paragraph("Comparaisons des sous-domaines inter-domaines", subtitle_style))
        
        # Style pour les cellules avec beaucoup de texte - nom unique
        compact_cell_style = ParagraphStyle(
            name='CompactCell_interdomaine',
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            wordWrap='CJK',
            alignment=0
        )
        
        # En-têtes en tant que paragraphes
        interdomaine_comparison_data = [[
            Paragraph("<b>Sous-domaine 1</b>", compact_cell_style),
            Paragraph("<b>Domaine</b>", compact_cell_style),
            Paragraph("<b>Note</b>", compact_cell_style),
            Paragraph("<b><, >, =</b>", compact_cell_style),
            Paragraph("<b>Note</b>", compact_cell_style),
            Paragraph("<b>Sous-domaine 2</b>", compact_cell_style),
            Paragraph("<b>Domaine</b>", compact_cell_style),
            Paragraph("<b>Diff.</b>", compact_cell_style),
            Paragraph("<b>Signif.</b>", compact_cell_style),
            Paragraph("<b>Fréq.</b>", compact_cell_style)
        ]]
        
        for comparison in interdomaine_comparisons:
            interdomaine_comparison_data.append([
                Paragraph(comparison['sous_domaine1'], compact_cell_style),
                Paragraph(comparison['domaine1'], compact_cell_style),
                Paragraph(str(comparison['note1']), compact_cell_style),
                Paragraph(comparison['signe'], compact_cell_style),
                Paragraph(str(comparison['note2']), compact_cell_style),
                Paragraph(comparison['sous_domaine2'], compact_cell_style),
                Paragraph(comparison['domaine2'], compact_cell_style),
                Paragraph(str(comparison['difference']), compact_cell_style),
                Paragraph("✓" if comparison['est_significatif'] else "-", compact_cell_style),
                Paragraph(comparison['frequence'] if comparison['frequence'] else "-", compact_cell_style)
            ])
        
        # Ajuster les largeurs pour accommoder les colonnes supplémentaires
        interdomaine_comparison_table = Table(interdomaine_comparison_data, 
                                                 colWidths=[2.5*cm, 2.5*cm, 1*cm, 1*cm, 1*cm, 2.5*cm, 2.5*cm, 1.5*cm, 1.5*cm, 1.5*cm])
        interdomaine_comparison_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (2, 1), (4, -1), 'CENTER'),
            ('ALIGN', (7, 1), (9, -1), 'CENTER'),
            ('BACKGROUND', (3, 1), (3, -1), colors.lightgrey),
        ]))
        
        elements.append(interdomaine_comparison_table)
    
    # Créer et sauvegarder le PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response



# import des données du tableau D.2 avec format éditable
@login_required
def import_frequence_domaine_data(request):
    """Vue temporaire pour importer les données du tableau D.2 avec format éditable"""
    from polls.models import Domain, Formulaire
    from django.db import transaction
    
    # Structure par tranche d'âge
    age_ranges = ["1-2", "3-6", "7-18", "19-49", "50-90"]
    
    # Niveaux de fréquence
    frequency_levels = ["16", "10", "5"]
    
    # Paires de domaines dans l'ordre de l'image
    domain_pairs = [
        ("Communication", "Vie quotidienne"),
        ("Communication", "Socialisation"),
        ("Communication", "Motricité"),
        ("Vie quotidienne", "Socialisation"),
        ("Vie quotidienne", "Motricité"),
        ("Socialisation", "Motricité")
    ]
    
    # Valeurs initiales du tableau D.2 (structurées par âge, fréquence, paire)
    initial_values = {}
    
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        # Récupération du formulaire Vineland
        formulaire_vineland = Formulaire.objects.filter(title__icontains='Vineland').first()
        if not formulaire_vineland:
            error_message = "Formulaire Vineland non trouvé. Vérifiez qu'un formulaire avec 'Vineland' dans le titre existe."
        else:
            # Récupération des domaines
            domains = {}
            for domain_name in ["Communication", "Vie quotidienne", "Socialisation", "Motricité"]:
                domain = Domain.objects.filter(formulaire=formulaire_vineland, name=domain_name).first()
                if domain:
                    domains[domain_name] = domain
                else:
                    # Afficher tous les domaines pour le débogage
                    all_domains = Domain.objects.filter(formulaire=formulaire_vineland)
                    print(f"Tous les domaines disponibles: {[d.name for d in all_domains]}")
                    
                    # Essayer avec un nom similaire
                    for d in all_domains:
                        if domain_name.lower() in d.name.lower():
                            domains[domain_name] = d
                            break
            
            # Vérification que tous les domaines sont trouvés
            missing_domains = [name for name in ["Communication", "Vie quotidienne", "Socialisation", "Motricité"] 
                                if name not in domains]
            
            if missing_domains:
                error_message = f"Domaines manquants: {', '.join(missing_domains)}"
                # Afficher les domaines trouvés pour aider au débogage
                error_message += f"\nDomaines trouvés: {', '.join([f'{k}: {v.name}' for k, v in domains.items()])}"
            else:
                # Import des données directement depuis le dictionnaire statique
                created_count = 0
                error_count = 0
                skipped_count = 0
                
                # Utiliser une transaction pour tout importer en une seule opération
                with transaction.atomic():
                    # Supprimer les anciennes données pour éviter les doublons
                    FrequenceDifferenceDomaineVineland.objects.all().delete()
                    
                    for age in age_ranges:
                        for pair in domain_pairs:
                            dom1, dom2 = pair
                            pair_key = f"{dom1}/{dom2}"
                            
                            # Vérifier si toutes les fréquences ont des valeurs pour cette combinaison
                            has_values = False
                            for freq in frequency_levels:
                                try:
                                    if initial_values[age][freq][pair_key] != "-":
                                        has_values = True
                                        break
                                except (KeyError, Exception):
                                    pass
                            
                            if has_values:
                                # Récupérer les valeurs pour chaque niveau de fréquence
                                freq_16 = initial_values[age]["16"][pair_key] if initial_values[age]["16"][pair_key] != "-" else None
                                freq_10 = initial_values[age]["10"][pair_key] if initial_values[age]["10"][pair_key] != "-" else None
                                freq_5 = initial_values[age]["5"][pair_key] if initial_values[age]["5"][pair_key] != "-" else None
                                
                                try:
                                    # Créer l'enregistrement
                                    FrequenceDifferenceDomaineVineland.objects.create(
                                        age=age,
                                        domaine1=domains[dom1],
                                        domaine2=domains[dom2],
                                        frequence_16=freq_16,
                                        frequence_10=freq_10,
                                        frequence_5=freq_5
                                    )
                                    created_count += 1
                                except Exception as e:
                                    error_count += 1
                                    print(f"Erreur pour {age}, {dom1}/{dom2}: {str(e)}")
                            else:
                                skipped_count += 1
                
                success_message = f"{created_count} fréquences importées avec succès, {error_count} erreurs, {skipped_count} ignorées"
    
    # Compte le nombre d'enregistrements déjà existants
    existing_count = FrequenceDifferenceDomaineVineland.objects.count()
    
    # Préparer le contexte avec un message initial si des données existent déjà
    context = {
        'age_ranges': age_ranges,
        'frequency_levels': frequency_levels,
        'domain_pairs': domain_pairs,
        'values': initial_values,
        'existing_count': existing_count
    }
    
    if existing_count > 0:
        context['info'] = f"Il y a déjà {existing_count} fréquences dans la base de données. Cliquer sur 'Importer' pour remplacer ces données."
    
    if error_message:
        context['error'] = error_message
    if success_message:
        context['success'] = success_message
    
    return render(request, 'vineland/import_frequence_data.html', context)

@login_required
def import_frequence_sous_domaine_data(request):
    """Vue pour importer les données du tableau D.4 avec format éditable"""
    
    # Structure par tranche d'âge
    age_ranges = ["1-2", "3-6", "7-18", "19-49", "50-90"]
    
    # Niveaux de fréquence
    frequency_levels = ["16", "10", "5"]
    
    # Liste des sous-domaines dans l'ordre des tableaux
    sous_domaines = [
        "Réceptive", "Expressive", "Écrite",  # Communication
        "Personnelle", "Domestique", "Communautaire",  # Vie quotidienne
        "Relations interpersonnelles", "Jeu et temps libre", "Adaptation",  # Socialisation
        "Globale", "Fine"  # Motricité
    ]
    
    # Créer les paires de sous-domaines (toutes les combinaisons possibles)
    sous_domaine_pairs = []
    for i in range(len(sous_domaines)):
        for j in range(len(sous_domaines)):
            if i != j:  # Exclure les paires où les deux sous-domaines sont identiques
                sous_domaine_pairs.append((sous_domaines[i], sous_domaines[j]))
    
    # Dictionnaire vide pour stocker les valeurs
    initial_values = {}
    
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        # Récupération du formulaire Vineland
        formulaire_vineland = Formulaire.objects.filter(title__icontains='Vineland').first()
        if not formulaire_vineland:
            error_message = "Formulaire Vineland non trouvé. Vérifiez qu'un formulaire avec 'Vineland' dans le titre existe."
        else:
            # Récupération des sous-domaines
            sous_domaines_obj = {}
            for sous_domaine_name in sous_domaines:
                sous_domaine = SousDomain.objects.filter(domain__formulaire=formulaire_vineland, name=sous_domaine_name).first()
                if sous_domaine:
                    sous_domaines_obj[sous_domaine_name] = sous_domaine
                else:
                    # Essayer avec un nom similaire
                    all_sous_domaines = SousDomain.objects.filter(domain__formulaire=formulaire_vineland)
                    for sd in all_sous_domaines:
                        if sous_domaine_name.lower() in sd.name.lower():
                            sous_domaines_obj[sous_domaine_name] = sd
                            break
            
            # Vérification que tous les sous-domaines sont trouvés
            missing_sous_domaines = [name for name in sous_domaines if name not in sous_domaines_obj]
            
            if missing_sous_domaines:
                error_message = f"Sous-domaines manquants: {', '.join(missing_sous_domaines)}"
                # Afficher les sous-domaines trouvés pour aider au débogage
                error_message += f"\nSous-domaines trouvés: {', '.join([f'{k}: {v.name}' for k, v in sous_domaines_obj.items()])}"
            else:
                # Récupérer les données du formulaire
                data = {}
                for age in age_ranges:
                    data[age] = {}
                    for freq in frequency_levels:
                        data[age][freq] = {}
                        for pair in sous_domaine_pairs:
                            sd1, sd2 = pair
                            pair_key = f"{sd1}/{sd2}"
                            input_name = f"value_{age}_{freq}_{sd1}_{sd2}".replace(" ", "_")
                            if input_name in request.POST and request.POST[input_name].strip():
                                data[age][freq][pair_key] = request.POST[input_name].strip()
                            else:
                                data[age][freq][pair_key] = "-"
                
                # Import des données
                created_count = 0
                error_count = 0
                skipped_count = 0
                
                # Supprimer les anciennes données pour éviter les doublons
                # Nous le faisons AVANT de commencer à créer de nouveaux enregistrements
                FrequenceDifferenceSousDomaineVineland.objects.all().delete()
                
                # Traiter chaque paire individuellement sans transaction globale
                for age in age_ranges:
                    for pair in sous_domaine_pairs:
                        sd1, sd2 = pair
                        pair_key = f"{sd1}/{sd2}"
                        
                        # Vérifier si toutes les fréquences ont des valeurs pour cette combinaison
                        has_values = False
                        for freq in frequency_levels:
                            try:
                                if data[age][freq][pair_key] != "-":
                                    has_values = True
                                    break
                            except (KeyError, Exception):
                                pass
                        
                        if has_values:
                            # Récupérer les valeurs pour chaque niveau de fréquence
                            freq_16 = data[age]["16"][pair_key] if data[age]["16"][pair_key] != "-" else ""
                            freq_10 = data[age]["10"][pair_key] if data[age]["10"][pair_key] != "-" else ""
                            freq_5 = data[age]["5"][pair_key] if data[age]["5"][pair_key] != "-" else ""
                            
                            # Utiliser try/except pour chaque paire individuellement
                            try:
                                # Créer l'enregistrement
                                FrequenceDifferenceSousDomaineVineland.objects.create(
                                    age=age,
                                    sous_domaine1=sous_domaines_obj[sd1],
                                    sous_domaine2=sous_domaines_obj[sd2],
                                    frequence_16=freq_16,
                                    frequence_10=freq_10,
                                    frequence_5=freq_5
                                )
                                created_count += 1
                            except Exception as e:
                                error_count += 1
                                print(f"Erreur pour {age}, {sd1}/{sd2}: {str(e)}")
                        else:
                            skipped_count += 1
                
                success_message = f"{created_count} fréquences importées avec succès, {error_count} erreurs, {skipped_count} ignorées"
    
    # Compte le nombre d'enregistrements déjà existants
    existing_count = FrequenceDifferenceSousDomaineVineland.objects.count()
    
    # Construire le dictionnaire de valeurs pour affichage (si vide)
    if not initial_values:
        # Récupérer les données existantes
        existing_data = FrequenceDifferenceSousDomaineVineland.objects.all()
        for record in existing_data:
            age = record.age
            sd1 = record.sous_domaine1.name
            sd2 = record.sous_domaine2.name
            pair_key = f"{sd1}/{sd2}"
            
            if age not in initial_values:
                initial_values[age] = {}
            
            for freq in frequency_levels:
                if freq not in initial_values[age]:
                    initial_values[age][freq] = {}
                
                value = getattr(record, f"frequence_{freq}")
                initial_values[age][freq][pair_key] = value if value is not None else "-"
    
    # Préparer le contexte avec un message initial si des données existent déjà
    context = {
        'age_ranges': age_ranges,
        'frequency_levels': frequency_levels,
        'sous_domaine_pairs': sous_domaine_pairs,
        'sous_domaines': sous_domaines,
        'values': initial_values,
        'existing_count': existing_count
    }
    
    if existing_count > 0:
        context['info'] = f"Il y a déjà {existing_count} fréquences dans la base de données. Cliquer sur 'Importer' pour remplacer ces données."
    
    if error_message:
        context['error'] = error_message
    if success_message:
        context['success'] = success_message
    
    return render(request, 'vineland/import_frequence_sous_domaine_data.html', context)


@login_required
def import_comparaison_domaine_data(request):
    """Vue temporaire pour importer les données directement à partir des valeurs statiques"""
    from polls.models import Domain, Formulaire
    from django.db import transaction
    
    # Structure par âge et niveau de significativité
    age_ranges = ["1", "2", "3", "4", "5", "6", "7-8", "9-11", "12-14", "15-18", "19-29", "30-49", "50-90"]
    significance_levels = [".05", ".01"]
    
    # Paires de domaines dans l'ordre de l'image
    domain_pairs = [
        ("Communication", "Vie quotidienne"),
        ("Communication", "Socialisation"),
        ("Communication", "Motricité"),
        ("Vie quotidienne", "Socialisation"),
        ("Vie quotidienne", "Motricité"),
        ("Socialisation", "Motricité")
    ]
    
    # Valeurs initiales du tableau D.1 (structurées par âge, niveau, paire)
    initial_values = {}
    
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        # Récupération du formulaire Vineland
        formulaire_vineland = Formulaire.objects.filter(title__icontains='Vineland').first()
        if not formulaire_vineland:
            error_message = "Formulaire Vineland non trouvé. Vérifiez qu'un formulaire avec 'Vineland' dans le titre existe."
        else:
            # Récupération des domaines
            domains = {}
            for domain_name in ["Communication", "Vie quotidienne", "Socialisation", "Motricité"]:
                domain = Domain.objects.filter(formulaire=formulaire_vineland, name=domain_name).first()
                if domain:
                    domains[domain_name] = domain
                else:
                    # Essayer avec un nom similaire ou rechercher tous les domaines
                    all_domains = Domain.objects.filter(formulaire=formulaire_vineland)
                    print(f"Tous les domaines disponibles: {[d.name for d in all_domains]}")
                    
                    # Essayer de trouver un match approximatif
                    for d in all_domains:
                        if domain_name.lower() in d.name.lower():
                            domains[domain_name] = d
                            break
            
            # Vérification que tous les domaines sont trouvés
            missing_domains = [name for name in ["Communication", "Vie quotidienne", "Socialisation", "Motricité"] 
                              if name not in domains]
            
            if missing_domains:
                error_message = f"Domaines manquants: {', '.join(missing_domains)}"
                # Afficher tous les domaines trouvés pour aider au débogage
                error_message += f"\nDomaines trouvés: {', '.join([f'{k}: {v.name}' for k, v in domains.items()])}"
            else:
                # Import des données directement depuis le dictionnaire statique
                created_count = 0
                error_count = 0
                skipped_count = 0
                
                # Utiliser une transaction pour tout importer en une seule opération
                with transaction.atomic():
                    # Supprimer les anciennes données pour éviter les doublons
                    ComparaisonDomaineVineland.objects.all().delete()
                    
                    for age in age_ranges:
                        for level in significance_levels:
                            for pair in domain_pairs:
                                dom1, dom2 = pair
                                pair_key = f"{dom1}/{dom2}"
                                
                                # Obtenir la valeur depuis le dictionnaire statique
                                try:
                                    value = initial_values[age][level][pair_key]
                                    if value is not None:
                                        # Créer l'enregistrement
                                        ComparaisonDomaineVineland.objects.create(
                                            age=age,
                                            niveau_significativite=level,
                                            domaine1=domains[dom1],
                                            domaine2=domains[dom2],
                                            difference_requise=value
                                        )
                                        created_count += 1
                                    else:
                                        skipped_count += 1
                                except (KeyError, Exception) as e:
                                    error_count += 1
                                    print(f"Erreur pour {age}, {level}, {pair_key}: {str(e)}")
                
                success_message = f"{created_count} comparaisons importées avec succès, {error_count} erreurs, {skipped_count} ignorées"
    
    # Compte le nombre d'enregistrements déjà existants
    existing_count = ComparaisonDomaineVineland.objects.count()
    
    # Préparer le contexte avec un message initial si des données existent déjà
    context = {
        'age_ranges': age_ranges,
        'significance_levels': significance_levels,
        'domain_pairs': domain_pairs,
        'values': initial_values,
        'existing_count': existing_count
    }
    
    if existing_count > 0:
        context['info'] = f"Il y a déjà {existing_count} comparaisons dans la base de données. Cliquer sur 'Importer' pour remplacer ces données."
    
    if error_message:
        context['error'] = error_message
    if success_message:
        context['success'] = success_message
    
    return render(request, 'vineland/import_comparaison_table.html', context)


def verify_data(request):
    if request.method == 'POST':
        age_range = request.POST.get('age_range', '').strip()
        if not age_range:
            return render(request, 'vineland/verify_data.html', 
                        {'error': 'Veuillez entrer une plage d\'âge'})
            
        try:
            start, end = age_range.replace(':', '.').split('-')
            start_parts = [p for p in start.split('.') if p]
            end_parts = [p for p in end.split('.') if p]

            if not start_parts or not end_parts:
                raise ValueError("Format de plage d'âge invalide")

            filters = {
                'age_debut_annee': int(float(start_parts[0])),
                'age_debut_mois': int(float(start_parts[1])) if len(start_parts) > 1 else 0,
                'age_debut_jour': int(float(start_parts[2])) if len(start_parts) > 2 else (0 if len(start_parts) == 2 else int(float(start_parts[1]))),
                'age_fin_annee': int(float(end_parts[0])),
                'age_fin_mois': int(float(end_parts[1])) if len(end_parts) > 1 else 0,
                'age_fin_jour': int(float(end_parts[2])) if len(end_parts) > 2 else (0 if len(end_parts) == 2 else int(float(end_parts[1]))),
            }

            mappings = EchelleVMapping.objects.filter(**filters).order_by('-note_echelle_v', 'sous_domaine__name')
            data = {}
            
            for mapping in mappings:
                note = str(mapping.note_echelle_v)
                if note not in data:
                    data[note] = {}
                
                # Formatage conditionnel de la valeur
                if mapping.note_brute_min == mapping.note_brute_max:
                    formatted_value = str(mapping.note_brute_min)
                else:
                    formatted_value = f"{mapping.note_brute_min}-{mapping.note_brute_max}"
                
                data[note][mapping.sous_domaine.name] = formatted_value

            return render(request, 'vineland/data_table.html', {
                'data': data,
                'age_range': age_range,
                'sous_domaines': [
                    'Réceptive', 'Expressive', 'Écritee', 'Personnelle',
                    'Domestique', 'Communautaire', 'Relations interpersonnelles',
                    'Jeu et temps libre', 'Adaptation', 'Globale', 'Fine'
                ]
            })
        except Exception as e:
            return render(request, 'vineland/verify_data.html', {'error': str(e)})

    return render(request, 'vineland/verify_data.html')

@csrf_exempt
def update_mapping(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Parsing de la plage d'âge
            age_range = data['age_range']
            start, end = age_range.replace(':', '.').split('-')
            start_parts = start.split('.')
            end_parts = end.split('.')

            # Construire les filtres d'âge
            age_filters = {
                'age_debut_annee': int(float(start_parts[0])),
                'age_debut_mois': int(float(start_parts[1])) if len(start_parts) > 1 else 0,
                'age_debut_jour': int(float(start_parts[2])) if len(start_parts) > 2 else (0 if len(start_parts) == 2 else int(float(start_parts[1]))),
                'age_fin_annee': int(float(end_parts[0])),
                'age_fin_mois': int(float(end_parts[1])) if len(end_parts) > 1 else 0,
                'age_fin_jour': int(float(end_parts[2])) if len(end_parts) > 2 else (0 if len(end_parts) == 2 else int(float(end_parts[1]))),
            }

            # Récupérer le mapping avec tous les critères
            mapping = EchelleVMapping.objects.get(
                note_echelle_v=data['note_echelle_v'],
                sous_domaine__name=data['sous_domaine'],
                **age_filters  # Inclure les filtres d'âge
            )

            # Mise à jour des valeurs
            if '-' in data['value']:
                min_val, max_val = map(int, data['value'].split('-'))
            else:
                min_val = max_val = int(data['value'])
            
            mapping.note_brute_min = min_val
            mapping.note_brute_max = max_val
            mapping.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def intervalle_confiance_table_view(request):
    """
    Vue principale pour afficher et éditer les intervalles de confiance des sous-domaines
    """
    # Récupérer les sous-domaines du formulaire Vineland dans l'ordre spécifique
    try:
        formulaire_vineland = Formulaire.objects.get(title__icontains='Vineland')
        
        # Récupérer tous les sous-domaines du formulaire Vineland
        sous_domaines_vineland = SousDomain.objects.filter(
            domain__formulaire=formulaire_vineland
        ).select_related('domain')
        
        # Ordre souhaité des sous-domaines
        ordre_sous_domaines = [
            'Réceptive', 'Expressive', 'Écrite', 'Personnelle', 'Domestique', 
            'Communautaire', 'Relations interpersonnelles', 'Jeu et temps libre', 
            'Adaptation', 'Globale', 'Fine'
        ]
        
        # Organiser les sous-domaines dans l'ordre défini
        sous_domaines = []
        for nom in ordre_sous_domaines:
            sous_domaine = sous_domaines_vineland.filter(name=nom).first()
            if sous_domaine:
                sous_domaines.append(sous_domaine)
                
    except Formulaire.DoesNotExist:
        # Si le formulaire Vineland n'existe pas, récupérer tous les sous-domaines
        sous_domaines = SousDomain.objects.all().select_related('domain')[:11]
    
    # Récupérer tous les intervalles de confiance
    intervalles = IntervaleConfianceSousDomaine.objects.select_related('sous_domaine').all()
    
    # Organiser les données en structure de tableau
    # Structure: {age: {niveau_confiance: {sous_domaine_id: intervalle_value}}}
    data_structure = {}
    
    for intervalle in intervalles:
        age = intervalle.age
        niveau = intervalle.niveau_confiance
        sous_domaine_id = intervalle.sous_domaine.id
        
        if age not in data_structure:
            data_structure[age] = {}
        if niveau not in data_structure[age]:
            data_structure[age][niveau] = {}
        
        data_structure[age][niveau][sous_domaine_id] = intervalle.intervalle
    
    # Préparer le contexte pour le template
    context = {
        'sous_domaines': sous_domaines,
        'data_structure': data_structure,
        'tranches_age': IntervaleConfianceSousDomaine.TRANCHES_AGE,
        'niveaux_confiance': IntervaleConfianceSousDomaine.NIVEAUX_CONFIANCE,
    }
    
    return render(request, 'intervalle_confiance_table.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def update_intervalle_confiance(request):
    """
    Vue AJAX pour mettre à jour un intervalle de confiance
    """
    try:
        data = json.loads(request.body)
        age = data.get('age')
        niveau_confiance = int(data.get('niveau_confiance'))
        sous_domaine_id = int(data.get('sous_domaine_id'))
        nouvelle_valeur = data.get('valeur')
        
        # Validation de base
        if nouvelle_valeur == '' or nouvelle_valeur is None:
            nouvelle_valeur = None
        else:
            nouvelle_valeur = int(nouvelle_valeur)
            if nouvelle_valeur < 0:
                return JsonResponse({
                    'success': False, 
                    'error': 'La valeur doit être positive'
                })
        
        # Récupérer le sous-domaine
        try:
            sous_domaine = SousDomain.objects.get(id=sous_domaine_id)
        except SousDomain.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'Sous-domaine non trouvé'
            })
        
        # Créer ou mettre à jour l'intervalle
        if nouvelle_valeur is not None:
            intervalle, created = IntervaleConfianceSousDomaine.objects.get_or_create(
                age=age,
                niveau_confiance=niveau_confiance,
                sous_domaine=sous_domaine,
                defaults={'intervalle': nouvelle_valeur}
            )
            
            if not created:
                intervalle.intervalle = nouvelle_valeur
                intervalle.save()
            
            action = "créé" if created else "mis à jour"
        else:
            # Si la valeur est vide, supprimer l'entrée existante
            try:
                intervalle = IntervaleConfianceSousDomaine.objects.get(
                    age=age,
                    niveau_confiance=niveau_confiance,
                    sous_domaine=sous_domaine
                )
                intervalle.delete()
                action = "supprimé"
            except IntervaleConfianceSousDomaine.DoesNotExist:
                action = "aucune action"
        
        return JsonResponse({
            'success': True, 
            'message': f'Intervalle {action} avec succès',
            'valeur': nouvelle_valeur
        })
        
    except ValueError as e:
        return JsonResponse({
            'success': False, 
            'error': 'Valeur invalide. Veuillez entrer un nombre entier.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': f'Erreur: {str(e)}'
        })

def export_intervalles_confiance(request):
    """
    Vue pour exporter les données au format JSON (optionnel)
    """
    intervalles = IntervaleConfianceSousDomaine.objects.select_related('sous_domaine').all()
    
    data = []
    for intervalle in intervalles:
        data.append({
            'age': intervalle.age,
            'niveau_confiance': intervalle.niveau_confiance,
            'sous_domaine': intervalle.sous_domaine.name,
            'intervalle': intervalle.intervalle
        })
    
    return JsonResponse({'data': data})
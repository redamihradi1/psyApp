from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from .models import QuestionVineland, ReponseVineland , PlageItemVineland , EchelleVMapping , NoteDomaineVMapping , IntervaleConfianceSousDomaine , IntervaleConfianceDomaine
from polls.models import Formulaire, Student, Questionnaire , SousDomain
from .utils.scoring import calculate_all_scores


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
    ).order_by(
    'created_at'  # Utilisation du timestamp de création pour l'ordre
    )

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

    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Gérer les données initiales
    initial_data = {}
    if request.session:
        for key in request.session.keys():
            if key.startswith('question_') or key == 'student':
                initial_data[key] = request.session[key]
    

    if request.method == 'POST':
        action = request.POST.get('action')
        print('action:', action)
        # Sauvegarder les réponses dans la session
        for key, value in request.POST.items():
            if key.startswith('question_') or key == 'student':
                request.session[key] = value

        # Vérifier les questions non répondues sur la page courante
        current_page_questions = page_obj.object_list
        unanswered_current = []
        for question in current_page_questions:
            key = f'question_{question.numero_item}'
            if key not in request.POST:
                unanswered_current.append(question.numero_item)

        if unanswered_current:
            messages.info(request, f"Questions sans réponse sur cette page : {', '.join(map(str, unanswered_current))}")

        if action == 'previous':
            prev_page = int(page_number) - 1
            return redirect(f'{request.path}?page={prev_page}')
            
        elif action == 'next':
            next_page = int(page_number) + 1
            return redirect(f'{request.path}?page={next_page}')
            
        elif action == 'submit':
            # Vérifier la sélection de l'étudiant
            if 'student' not in request.session:
                messages.error(request, "Veuillez sélectionner un étudiant")
                return redirect(request.path)

            # Vérifier les questions non répondues
            all_unanswered = []
            for question in questions:
                if f'question_{question.numero_item}' not in request.session:
                    all_unanswered.append(question.numero_item)

            if all_unanswered:
                messages.warning(request, f"Questions sans réponse dans le questionnaire : {', '.join(map(str, all_unanswered))}")

            # Créer le questionnaire
            student = get_object_or_404(Student, id=request.session['student'])
            print('student:', student)
            messages.success(request, "Questionnaire complété avec succès!")
            questionnaire = Questionnaire.objects.create(
                formulaire=formulaire,
                student=student,
                parent=parent,
                created_at=timezone.now(),
            )

            # Process all answers from session
            for key, value in request.session.items():
                if key.startswith('question_'):
                    question_num = int(key.split('_')[1])
                    question = QuestionVineland.objects.get(numero_item=question_num)
                    if isinstance(value, int):
                        value = str(value)
                    # Vérifier si la valeur est dans les choix valides
                    valid_values = [str(choice[0]) for choice in QuestionVineland.CHOIX_REPONSES]
                    if value in valid_values or value in ['NSP', 'NA', '?', '']:
                        reponse = ReponseVineland(
                            question=question,
                            questionnaire=questionnaire,
                            reponse=value
                        )
                        reponse.save()
            
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
    
    # Calculer l'âge de l'étudiant au moment du questionnaire
    age_at_test = questionnaire.created_at.date() - student.date_of_birth
    age_years = age_at_test.days // 365
    remaining_days = age_at_test.days % 365
    age_months = remaining_days // 30
    age_days = remaining_days % 30

    echelle_v_scores = {}
    
    for domain_name, domain_scores in scores.items():
        # Exclure le domaine "Comportements problématiques"
        if domain_name != "Comportements problématiques":
            echelle_v_scores[domain_name] = {}
            for sous_domain, score in domain_scores.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Rechercher la correspondance d'échelle-V appropriée
                echelle_v = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    age_debut_annee__lte=age_years,
                    age_fin_annee__gte=age_years,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                ).first()
                
                if echelle_v:
                    echelle_v_scores[domain_name][sous_domain] = {
                        'note_brute': score['note_brute'],
                        'note_echelle_v': echelle_v.note_echelle_v
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
    
    # Calculer l'âge de l'étudiant
    age_at_test = questionnaire.created_at.date() - student.date_of_birth
    age_years = age_at_test.days // 365
    remaining_days = age_at_test.days % 365
    age_months = remaining_days // 30
    age_days = remaining_days % 30
    
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

    # Structure pour stocker les résultats
    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            domain_data = {
                'name': domain_name,
                'sous_domaines': [],
                'domain_score': None
            }
            
            # Calculer la somme des notes échelle-v pour le domaine
            domain_note_v_sum = 0
            
            # Traitement des sous-domaines
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                echelle_v = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    age_debut_annee__lte=age_years,
                    age_fin_annee__gte=age_years,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                ).first()
                
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

            # Obtenir le mapping du domaine
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
    
    # Récupérer les niveaux de confiance pour chaque domaine depuis la requête
    domain_confidence_levels = {}
    for key, value in request.GET.items():
        if key.startswith('niveau_confiance_'):
            domain_name = key.replace('niveau_confiance_', '')
            domain_confidence_levels[domain_name] = int(value)
    
    # Calculer l'âge de l'étudiant
    age_at_test = questionnaire.created_at.date() - student.date_of_birth
    age_years = age_at_test.days // 365
    remaining_days = age_at_test.days % 365
    age_months = remaining_days // 30
    age_days = remaining_days % 30
    
    # Déterminer les tranches d'âge
    if age_years < 3:
        tranche_age = '1-2'
        tranche_age_intervalle = '1'
    elif age_years < 7:
        tranche_age = '3-6'
        tranche_age_intervalle = str(age_years)
    elif age_years < 9:
        tranche_age = '7-18'
        tranche_age_intervalle = '7-8'
    elif age_years < 12:
        tranche_age = '7-18'
        tranche_age_intervalle = '9-11'
    elif age_years < 15:
        tranche_age = '7-18'
        tranche_age_intervalle = '12-14'
    elif age_years < 19:
        tranche_age = '7-18'
        tranche_age_intervalle = '15-18'
    elif age_years < 30:
        tranche_age = '19-29'
        tranche_age_intervalle = '19-29'
    elif age_years < 50:
        tranche_age = '30-49'
        tranche_age_intervalle = '30-49'
    else:
        tranche_age = '50-90'
        tranche_age_intervalle = '50-90'

    complete_scores = []
    
    for domain_name, domain_scores_data in scores.items():
        if domain_name != "Comportements problématiques":
            # Niveau de confiance pour ce domaine (par défaut 95)
            niveau_confiance = domain_confidence_levels.get(domain_name.replace(' ', '_'), 90)
            
            domain_data = {
                'name': domain_name,
                'name_slug': domain_name.replace(' ', '_'),
                'niveau_confiance': niveau_confiance,
                'sous_domaines': [],
                'domain_score': None
            }
            
            # Calculer la somme des notes échelle-v pour le domaine
            domain_note_v_sum = 0
            
            for sous_domain, score in domain_scores_data.items():
                sous_domain_obj = SousDomain.objects.get(name=sous_domain)
                
                # Obtenir l'échelle-V
                echelle_v = EchelleVMapping.objects.filter(
                    sous_domaine=sous_domain_obj,
                    age_debut_annee__lte=age_years,
                    age_fin_annee__gte=age_years,
                    note_brute_min__lte=score['note_brute'],
                    note_brute_max__gte=score['note_brute']
                ).first()
                
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

            # Obtenir le mapping et l'intervalle du domaine
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
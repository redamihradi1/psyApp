from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from .models import QuestionVineland, ReponseVineland , PlageItemVineland
from polls.models import Formulaire, Student, Questionnaire


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
        'sous_domaine__domain__name', 
        'sous_domaine__name', 
        'numero_item'
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
    print('request.method:', request.method)
    print('request.POST:', request.POST)

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
            questionnaire_key = f"{parent.name}-{student.name}-{timezone.now().strftime('%d%m%Y')}"
            
            messages.success(request, "Questionnaire complété avec succès!")
            
            # Nettoyer la session
            for key in list(request.session.keys()):
                if key.startswith('question_') or key == 'student':
                    del request.session[key]

            messages.success(request, "Questionnaire complété avec succès!")
            # return redirect('vineland_summary', questionnaire_id=questionnaire.id)

    return render(request, 'vineland/questionnaire.html', {
        'formulaire': formulaire,
        'students': students,
        'page_obj': page_obj,
        'initial_data': initial_data,
    })
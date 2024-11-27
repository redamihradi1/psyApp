from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Formulaire, Question, Domain, SousDomain,Student,Parent,Response,SousDomaineResponse,DomaineResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login


# @login_required
# def questionnaire_view(request, formulaire_id):
#     print("Start questionnaire view")
#     formulaire = get_object_or_404(Formulaire, id=formulaire_id)
#     parent = get_object_or_404(Parent, user_name=request.user.username)
#     students = parent.students.all()
#     domains = Domain.objects.filter(formulaire=formulaire)
#     sousdomains = SousDomain.objects.filter(domain__in=domains)
#     # the qustion shoul be order by id to be in the same order as the questionnaire
#     questions = Question.objects.filter(sous_domain__in=sousdomains).order_by('num_question')
    
#     paginator = Paginator(questions, 15) 
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

    
#     initial_data = {}
#     for key in request.session:
#         if key.startswith('question_') or key == 'student':
#             initial_data[key] = request.session[key]


#     if request.method == 'POST':
        
#         for key in form_keys:
#             if key in request.POST:
#                 request.session[key] = request.POST[key]
#                 print(f"key: {key}, value: {request.POST[key]}")
                
#         # Si c'est la dernière page, traiter le formulaire
#         if int(page_number) == paginator.num_pages:

#             student_id = request.POST.get('student')
#             student = get_object_or_404(Student, id=student_id)
#             print("student", student)
#             ukey = f"{parent.name}-{student.name}-{timezone.now().strftime('%d%m%Y')}"
#             questionnaire = Questionnaire.objects.create(
#                 parent=parent,
#                 student=student,
#                 formulaire=formulaire,
#                 created_at=timezone.now(),
#             )
#             questionnaire.unique_key = ukey
#             questionnaire.save()

#             sousdomaines = SousDomain.objects.filter(domain__formulaire=formulaire)
#             print("How many sousdomaines", len(sousdomaines))
#             for sousdomaine in sousdomaines:
#                 questions = Question.objects.filter(sous_domain=sousdomaine)
#                 score_sousdomaine = 0
#                 # Calcul de la somme des réponses pour ce sous-domaine
#                 for question in questions:
#                     if question.can_ask:
#                         answer = request.POST.get(f'question_{question.num_question}', 0)
#                         # check if the answer is number and it not empty
#                         if answer == '' or answer is None:
#                             answer = 0
#                         score_sousdomaine += int(answer)
#                         response = Response(questionnaire=questionnaire, question=question, answer=int(answer))
#                         response.save()
#                 sous_domaine_response = SousDomaineResponse.objects.create(
#                     sous_domaine=sousdomaine,
#                     questionnaire=questionnaire,
#                     score_total=score_sousdomaine
#                 )

#             domaines = Domain.objects.filter(formulaire=formulaire)
#             print("How many domaines", len(domaines))
#             for domaine in domaines:
#                 sous_domaines = domaine.sousdomain_set.all()
#                 score_domaine = 0
#                 # Additionner les scores des sous-domaines appartenant à ce domaine
#                 for sousdomaine in sous_domaines:
#                     sous_domaine_response = SousDomaineResponse.objects.get(
#                         sous_domaine=sousdomaine,
#                         questionnaire=questionnaire
#                     )
#                     score_domaine += sous_domaine_response.score_total
#                 # Sauvegarder le score total du domaine dans DomaineResponse
#                 domaine_response = DomaineResponse.objects.create(
#                     domaine=domaine,
#                     questionnaire=questionnaire,
#                     score_total=score_domaine
#                 )
#                 domaine_response.save()

#             return redirect('success_view')
            
#     return render(request, 'questionnaire_form.html', {
#         'formulaire': formulaire,
#         'students': students,
#         'page_obj': page_obj,
#     })

@login_required
def questionnaire_view(request, formulaire_id):
    print("Start questionnaire view")
    formulaire = get_object_or_404(Formulaire, id=formulaire_id)
    parent = get_object_or_404(Parent, user_name=request.user.username)
    students = parent.students.all()
    domains = Domain.objects.filter(formulaire=formulaire)
    sousdomains = SousDomain.objects.filter(domain__in=domains)
    questions = Question.objects.filter(sous_domain__in=sousdomains).order_by('num_question')
    
    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Initialize context with session data
    initial_data = {}
    if request.session:
        for key in request.session.keys():
            if key.startswith('question_') or key == 'student':
                initial_data[key] = request.session[key]

    if request.method == 'POST':
        # Save form data to session
        for key, value in request.POST.items():
            if key.startswith('question_') or key == 'student':
                request.session[key] = value

        current_page_questions = page_obj.object_list
        for question in current_page_questions:
            if question.can_ask:
                key = f'question_{question.num_question}'
                if key not in request.POST:
                    messages.error(request, f"Veuillez répondre à toutes les questions de cette page")
                    return redirect(request.path + f'?page={page_number}')

        if int(page_number) == paginator.num_pages:
            # Process final submission
            #check if all questions are answered
            print("Check questionnaire x1")
            if not check_questionnaire(questions,request):
                unanswered = [q.num_question for q in questions if q.can_ask and f'question_{q.num_question}' not in request.session]
                messages.error(request, f"Questions non répondues: {', '.join(map(str, unanswered))}")
                return redirect(request.path)

            student = get_object_or_404(Student, id=request.session['student'])
            ukey = f"{parent.name}-{student.name}-{timezone.now().strftime('%d%m%Y')}"
            
            questionnaire = Questionnaire.objects.create(
                parent=parent,
                student=student,
                formulaire=formulaire,
                created_at=timezone.now(),
                unique_key=ukey
            )

            # Process all answers from session
            for key, value in request.session.items():
                if key.startswith('question_'):
                    question_num = int(key.split('_')[1])
                    question = get_object_or_404(Question, num_question=question_num)
                    if question.can_ask:
                        answer = int(value) if value else 0
                        Response.objects.create(
                            questionnaire=questionnaire,
                            question=question,
                            answer=answer
                        )

            # Calculate scores for sous-domaines
            for sousdomaine in sousdomains:
                questions = Question.objects.filter(sous_domain=sousdomaine)
                score = sum(
                    int(request.session.get(f'question_{q.num_question}', 0))
                    for q in questions if q.can_ask
                )
                SousDomaineResponse.objects.create(
                    sous_domaine=sousdomaine,
                    questionnaire=questionnaire,
                    score_total=score
                )

            # Calculate scores for domaines
            for domaine in domains:
                score = sum(
                    resp.score_total
                    for resp in SousDomaineResponse.objects.filter(
                        questionnaire=questionnaire,
                        sous_domaine__domain=domaine
                    )
                )
                DomaineResponse.objects.create(
                    domaine=domaine,
                    questionnaire=questionnaire,
                    score_total=score
                )

            # Clear session after successful submission
            for key in list(request.session.keys()):
                if key.startswith('question_') or key == 'student':
                    del request.session[key]

            return redirect('success_view')

        # Redirect to next page
        next_page = int(page_number) + 1
        return redirect(f'{request.path}?page={next_page}')

    return render(request, 'questionnaire_form.html', {
        'formulaire': formulaire,
        'students': students,
        'page_obj': page_obj,
        'initial_data': initial_data,
    })



def check_questionnaire(questions, request):
    print("Check questionnaire")
    for question in questions:
        if question.can_ask:
            key = f'question_{question.num_question}'
            if key not in request.session:
                print(f"Missing answer for question {question.num_question}")
                return False
    return True

def success_view(request):
    return render(request, 'questionnaire/success.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect to the questionnaire view
            return redirect('questionnaire_view', formulaire_id=1)
        else:
            # Affiche un message d'erreur si l'authentification échoue
            return render(request, 'login.html', {'error': 'Nom d’utilisateur ou mot de passe incorrect'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    formulaires = Formulaire.objects.all()
    questionnaires = Questionnaire.objects.filter(parent__user_name=request.user.username)
    return render(request, 'home.html', {
        'formulaires': formulaires,
        'questionnaires': questionnaires
    })
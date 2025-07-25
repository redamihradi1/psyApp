from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Formulaire, Question, Domain, SousDomain,Student,Parent,Response,SousDomaineResponse,DomaineResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.http import HttpResponse
from .utils.pdf_generator import generate_questionnaire_pdf
from .utils.score_calculator import ScoreCalculator
from .forms import ParentForm, StudentForm
from django.core.exceptions import ValidationError
from django.db import transaction



@login_required
def questionnaire_view(request, formulaire_id):
    formulaire = get_object_or_404(Formulaire, id=formulaire_id)
    parent = request.user
    #get all students if superuser else get students of parent
    if parent.is_superuser:
        students = Student.objects.all()
    else:
        students = Student.objects.filter(parent=parent)
    domains = Domain.objects.filter(formulaire=formulaire)
    sousdomains = SousDomain.objects.filter(domain__in=domains)
    questions = Question.objects.filter(sous_domain__in=sousdomains).order_by('num_question')
    
    paginator = Paginator(questions, 29)
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

            clear_session_data(request.session)
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


            return redirect('questionnaire_summary', questionnaire_id=questionnaire.id)
            # return redirect('success_view')

        # Redirect to next page
        next_page = int(page_number) + 1
        return redirect(f'{request.path}?page={next_page}')
        
    
    initial_data = {}
    for key in request.session.keys():
        if key.startswith('question_') or key == 'student':
            initial_data[key] = request.session[key]

    return render(request, 'questionnaire_form.html', {
        'formulaire': formulaire,
        'students': students,
        'page_obj': page_obj,
        'initial_data': initial_data,
        'visited_pages': request.session.get('visited_pages', [])
    })

def clear_session_data(session):
    session_keys = [key for key in session.keys() if key.startswith('question_') or key == 'student']
    for key in session_keys:
        del session[key]

def summary_view(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    
    domains = Domain.objects.filter(formulaire=questionnaire.formulaire).exclude(name='Autre')
    summary_data = []
    
    for domain in domains:
        sous_domains = SousDomain.objects.filter(domain=domain).exclude(name='Autre')
        sous_domain_data = []
        domain_total = 0
        
        for sous_domain in sous_domains:
            responses = Response.objects.filter(
                questionnaire=questionnaire,
                question__sous_domain=sous_domain
            )
            
            zeros = responses.filter(answer=0).count()
            ones = responses.filter(answer=1).count()
            twos = responses.filter(answer=2).count()
            total = (zeros * 0) + (ones * 1) + (twos * 2)
            domain_total += total
            
            sous_domain_data.append({
                'name': sous_domain.name,
                'zeros': zeros,
                'ones': ones,
                'twos': twos,
                'total': total
            })
        
        summary_data.append({
            'domain': domain.name,
            'sous_domains': sous_domain_data,
            'domain_total': domain_total
        })
    
    return render(request, 'summary.html', {
        'questionnaire': questionnaire,
        'summary_data': summary_data
    })

def detailed_summary_view(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    domains = Domain.objects.filter(formulaire=questionnaire.formulaire).exclude(name='Autre')
    
    summary_data = []
    for domain in domains:
        sous_domains = SousDomain.objects.filter(domain=domain).exclude(name='Autre')
        sous_domain_data = []
        
        for sous_domain in sous_domains:
            responses = Response.objects.filter(
                questionnaire=questionnaire,
                question__sous_domain=sous_domain
            ).select_related('question')
            
            questions_by_answer = {
                0: responses.filter(answer=0),
                1: responses.filter(answer=1),
                2: responses.filter(answer=2)
            }
            
            sous_domain_data.append({
                'name': sous_domain.name,
                'responses': questions_by_answer
            })
            
        summary_data.append({
            'domain': domain.name,
            'sous_domains': sous_domain_data
        })
    
    return render(request, 'questionnaire/detailed_summary.html', {
        'questionnaire': questionnaire,
        'summary_data': summary_data
    })


def calculate_scores(request, questionnaire_id):
    try:
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        calculator = ScoreCalculator(questionnaire.student, questionnaire)
        resultat_final, deuxieme_tableau = calculator.calculate()
        
        context = {
            'questionnaire': questionnaire,
            'resultat_final': resultat_final,
            'deuxieme_tableau': deuxieme_tableau
        }
        
        return render(request, 'questionnaire/score_results.html', context)
        
    except Exception as e:
        messages.error(request, f"An error occurred while calculating scores: {str(e)}")
        return redirect('home')

def generate_pdf(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    domains = Domain.objects.filter(formulaire=questionnaire.formulaire).exclude(name='Autre')
    sous_domains = SousDomain.objects.exclude(name='Autre')
    responses = Response.objects.filter(questionnaire=questionnaire).select_related('question')
    
    pdf = generate_questionnaire_pdf(questionnaire, domains, sous_domains, responses)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="questionnaire_{questionnaire_id}.pdf"'
    response.write(pdf)
    return response

def check_questionnaire(questions, request):
    for question in questions:
        if question.can_ask:
            key = f'question_{question.num_question}'
            if key not in request.session:
                return False
    return True

def success_view(request):
    return render(request, 'simpleUser/success.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def home_view(request):
    formulaires = Formulaire.objects.all()
    
    # Filtrer les questionnaires selon l'utilisateur
    if request.user.is_superuser:
        pep3_list = Questionnaire.objects.filter(formulaire__title='PEP3').order_by('-created_at')
        vineland_list = Questionnaire.objects.filter(formulaire__title='Vineland').order_by('-created_at')
    else:
        pep3_list = Questionnaire.objects.filter(
            parent=request.user,
            formulaire__title='PEP3'
        ).order_by('-created_at')
        vineland_list = Questionnaire.objects.filter(
            parent=request.user,
            formulaire__title='Vineland'
        ).order_by('-created_at')
    
    # Pagination pour PEP3
    pep3_paginator = Paginator(pep3_list, 5)
    pep3_page = request.GET.get('pep3_page', 1)
    pep3_questionnaires = pep3_paginator.get_page(pep3_page)
    
    # Pagination pour Vineland
    vineland_paginator = Paginator(vineland_list, 5)
    vineland_page = request.GET.get('vineland_page', 1)
    vineland_questionnaires = vineland_paginator.get_page(vineland_page)
    
    context = {
        'formulaires': formulaires,
        'pep3_questionnaires': pep3_questionnaires,
        'vineland_questionnaires': vineland_questionnaires,
        'pep3_paginator': pep3_paginator,
        'vineland_paginator': vineland_paginator,
    }
    
    return render(request, 'home.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    # Stats existantes    
    total_parents = Parent.objects.filter(is_parent=True).count()
    total_students = Student.objects.count()
    
    formulaire_stats = Formulaire.objects.annotate(
        total_questionnaires=Count('questionnaire')
    )
    
    # Pagination pour les parents
    parents_list = Parent.objects.filter(is_parent=True).order_by('-date_joined')
    parents_paginator = Paginator(parents_list, 4)
    parents_page = request.GET.get('parents_page')
    parents = parents_paginator.get_page(parents_page)
    
    # Pagination pour les étudiants
    students_list = Student.objects.all().order_by('-id')
    students_paginator = Paginator(students_list, 4)
    students_page = request.GET.get('students_page')
    students = students_paginator.get_page(students_page)
    
    # recent_questionnaires = Questionnaire.objects.select_related(
    #     'parent', 'student', 'formulaire'
    # ).order_by('-created_at')[:5]
    
    context = {
        'total_parents': total_parents,
        'total_students': total_students,
        'formulaire_stats': formulaire_stats,
        'parents': parents,
        'students': students
    }
    return render(request, 'admin/base_admin_dashboard.html', context)

@login_required
def create_parent(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    if request.method == 'POST':
        form = ParentForm(request.POST)
        if form.is_valid():
            parent = form.save(commit=False)
            parent.is_parent = True
            parent.set_password(form.cleaned_data['password'])
            parent.save()
            messages.success(request, 'Parent créé avec succès')
            return redirect('admin_dashboard')
    else:
        form = ParentForm()
    
    return render(request, 'admin/parent_form.html', {'form': form, 'action': 'Créer'})

@login_required
def edit_parent(request, parent_id):
    if not request.user.is_superuser:
        return redirect('home')
        
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        form = ParentForm(request.POST, instance=parent)
        if form.is_valid():
            parent = form.save(commit=False)
            if form.cleaned_data.get('password'):
                parent.set_password(form.cleaned_data['password'])
            parent.save()
            messages.success(request, 'Parent modifié avec succès')
            return redirect('admin_dashboard')
    else:
        form = ParentForm(instance=parent)
    
    return render(request, 'admin/parent_form.html', {'form': form, 'action': 'Modifier'})

@login_required
def create_student(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Étudiant créé avec succès')
            return redirect('admin_dashboard')
    else:
        form = StudentForm()
    
    return render(request, 'admin/student_form.html', {'form': form, 'action': 'Créer'})

@login_required
def edit_student(request, student_id):
    if not request.user.is_superuser:
        return redirect('home')
        
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Étudiant modifié avec succès')
            return redirect('admin_dashboard')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'admin/student_form.html', {'form': form, 'action': 'Modifier'})
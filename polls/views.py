from django.shortcuts import render, get_object_or_404, redirect
from .models import Questionnaire, Formulaire, Question, Domain, SousDomain,Student,Parent,Response,SousDomaineResponse,DomaineResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login



@login_required
def questionnaire_view(request, formulaire_id):
    print("Start questionnaire view")
    formulaire = get_object_or_404(Formulaire, id=formulaire_id)
    parent = request.user
    print("Parent => ", parent)
    #get all students
    students = Student.objects.all()
    print("Students", students)
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
        print("user", user)
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
    questionnaires = Questionnaire.objects.filter(parent=request.user)
    print("Current user", request.user)
    print("Questionnaires size", len(questionnaires))
    for questionnaire in questionnaires:
        print("Questionnaire parent", questionnaire.parent)
    return render(request, 'home.html', {
        'formulaires': formulaires,
        'questionnaires': questionnaires
    })
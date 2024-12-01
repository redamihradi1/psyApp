# vineland/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from .models import QuestionVineland, ReponseVineland, PlageItemVineland
from polls.models import Formulaire, Student , Questionnaire

@login_required
def vineland_questionnaire(request, formulaire_id):
    formulaire = get_object_or_404(Formulaire, id=formulaire_id)
    parent = request.user
    
    if parent.is_superuser:
        students = Student.objects.all()
    else:
        students = Student.objects.filter(parent=parent)
    
    questions = QuestionVineland.objects.select_related('sous_domaine').order_by(
        'sous_domaine__domain__name', 
        'sous_domaine__name', 
        'numero_item'
    )

    
    
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    initial_data = {}
    if request.session:
        for key in request.session.keys():
            if key.startswith('question_') or key == 'student':
                initial_data[key] = request.session[key]

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question_') or key == 'student':
                request.session[key] = value

        if int(page_number) == paginator.num_pages:
            student = get_object_or_404(Student, id=request.session['student'])
            questionnaire_key = f"{parent.name}-{student.name}-{timezone.now().strftime('%d%m%Y')}"

            questionnaire = Questionnaire.objects.create(
                parent=parent,
                student=student,
                formulaire=formulaire,
                created_at=timezone.now(),
                unique_key=questionnaire_key
            )

            for key, value in request.session.items():
                if key.startswith('question_'):
                    question_id = int(key.split('_')[1])
                    question = get_object_or_404(QuestionVineland, numero_item=question_id)
                    if value in ['0', '1', '2', 'N', 'S', 'P']:
                        ReponseVineland.objects.create(
                            questionnaire=questionnaire,
                            question=question,
                            reponse=value
                        )

            for key in list(request.session.keys()):
                if key.startswith('question_') or key == 'student':
                    del request.session[key]

            return redirect('vineland_summary', questionnaire_id=questionnaire.id)

        next_page = int(page_number) + 1
        return redirect(f'{request.path}?page={next_page}')

    return render(request, 'vineland/questionnaire.html', {
        'formulaire': formulaire,
        'students': students,
        'page_obj': page_obj,
        'initial_data': initial_data,
    })
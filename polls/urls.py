from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view , name='home'), 
    path('login/', login_view , name='login'),
    path('logout/', logout_view , name='logout'),
    path('register/', register_view , name='register'),
    path('questionnaire/<int:formulaire_id>/', questionnaire_view, name='questionnaire_view'),
    path('questionnaire/<int:questionnaire_id>/summary/', summary_view, name='questionnaire_summary'),
    path('questionnaire/<int:questionnaire_id>/detailed-summary/', detailed_summary_view, name='detailed_summary'),
    path('questionnaire/<int:questionnaire_id>/pdf/', generate_pdf, name='generate_pdf'),
    path('questionnaire/<int:questionnaire_id>/scores/', calculate_scores, name='calculate_scores'),
    path('questionnaire/success/', success_view, name='success_view'),  # URL for the success page

    path('admincustom/dashboard/', admin_dashboard, name='admin_dashboard'),

    path('admincustom/create-parent/', create_parent, name='create_parent'),
    path('admincustom/edit-parent/<int:parent_id>/', edit_parent, name='edit_parent'),
    path('admincustom/create-student/', create_student, name='create_student'),
    path('admincustom/edit-student/<int:student_id>/', edit_student, name='edit_student'),
]

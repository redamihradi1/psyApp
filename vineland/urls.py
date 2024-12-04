from django.urls import path
from django.contrib import admin
from . import views


app_name = 'vineland'

urlpatterns = [
    path('questionnaire/<int:formulaire_id>/', views.vineland_questionnaire, name='vineland_questionnaire'),
    path('questionnaire/<int:questionnaire_id>/scores/', views.vineland_scores, name='vineland_scores'),
    path('questionnaire/<int:questionnaire_id>/echelle-v/',  views.vineland_echelle_v, name='vineland_echelle_v'),
    path('domain-scores/<int:questionnaire_id>/', views.vineland_domain_scores, name='vineland_domain_scores'),
    path('confidence-intervals/<int:questionnaire_id>/', views.vineland_confidence_intervals, name='vineland_confidence_intervals'),
]
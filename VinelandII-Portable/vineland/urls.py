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
    path('niveaux-adaptatifs/<int:questionnaire_id>/', views.vineland_niveaux_adaptatifs, name='vineland_niveaux_adaptatifs'),
    path('questionnaire/<int:questionnaire_id>/age-equivalent/', views.vineland_age_equivalent, name='age_equivalent_view'),
    path('questionnaire/<int:questionnaire_id>/comparaisons-paires/', views.vineland_comparaisons_paires, name='vineland_comparaisons_paires'),
    path('export_pdf/<int:questionnaire_id>/', views.vineland_export_pdf, name='vineland_export_pdf'),


    # path('verify-data/', views.verify_data, name='verify_data'),
    # path('update-mapping/', views.update_mapping, name='update_mapping'),
    # path('import-comparaison-domaine/', views.import_comparaison_domaine_data, name='import_comparaison_domaine'), # all good
    # path('import-frequence-domaine/', views.import_frequence_domaine_data, name='import_frequence_domaine'),# all good
    # path('import-comparaison-sous-domaine/', views.import_comparaison_sous_domaine_data, name='import_comparaison_sous_domaine'),# all good
    # path('import-frequence-sous-domaine/', views.import_frequence_sous_domaine_data, name='import_frequence_sous_domaine_data'),
    # path('intervalle-confiance/', views.intervalle_confiance_table_view, name='intervalle_confiance_table'),
    # path('intervalle-confiance/update/', views.update_intervalle_confiance, name='update_intervalle_confiance'),
    # path('intervalle-confiance/export/', views.export_intervalles_confiance, name='export_intervalles_confiance')

]
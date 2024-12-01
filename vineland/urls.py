from django.urls import path
from django.contrib import admin
from . import views
from vineland.admin import vineland_admin


app_name = 'vineland'

urlpatterns = [
    path('questionnaire/<int:formulaire_id>/', views.vineland_questionnaire, name='vineland_questionnaire'),
]
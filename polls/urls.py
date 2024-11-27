from django.urls import path
from .views import questionnaire_view, success_view ,home_view, login_view , logout_view

urlpatterns = [
    path('', home_view , name='home'), 
    path('login/', login_view , name='login'),
    path('logout/', logout_view , name='logout'),
    path('questionnaire/<int:formulaire_id>/', questionnaire_view, name='questionnaire_view'),
    path('questionnaire/success/', success_view, name='success_view'),  # URL for the success page
]

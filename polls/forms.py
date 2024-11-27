from django import forms
from .models import Questionnaire

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['formulaire']  # Include 'formulaire' if you want to accept it

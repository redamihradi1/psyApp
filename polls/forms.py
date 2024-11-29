from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Questionnaire , Parent, Student

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['formulaire']  # Include 'formulaire' if you want to accept it

class ParentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False,
                                help_text="Laissez vide pour ne pas changer le mot de passe")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Parent
        fields = ['name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        
        if password:
            validate_password(password)

        return cleaned_data

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'parent', 'age', 'sexe', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
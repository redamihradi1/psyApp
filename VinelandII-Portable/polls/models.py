from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Parent(AbstractUser):
    name = models.CharField(max_length=255, default='')
    is_parent = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    class Meta:
        swappable = 'AUTH_USER_MODEL'

        
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    # parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255, default='', verbose_name='Nom de l’Élève')
    age = models.FloatField(default=1, verbose_name='Âge')
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M', verbose_name='Sexe')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date de Naissance')

    def __str__(self):
        return self.name

class Formulaire(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default='', verbose_name='Titre du Formulaire')
    description = models.TextField(default='', verbose_name='Description du Formulaire')

    def __str__(self):
        return self.title

class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    formulaire = models.ForeignKey(Formulaire, related_name='domains', on_delete=models.CASCADE, default='', verbose_name='Formulaire')
    name = models.CharField(max_length=255, default='', verbose_name='Nom du Domaine')

    def __str__(self):
        return self.name

class SousDomain(models.Model):
    id = models.AutoField(primary_key=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, default='', verbose_name='Domaine' ,related_name='sous_domaines')
    name = models.CharField(max_length=255, default='', verbose_name='Nom du Sous-Domaine')

    def __str__(self):
        return self.name

class Question(models.Model):
    num_question  = models.AutoField(primary_key=True, verbose_name='Numéro de la Question') 
    sous_domain = models.ForeignKey(SousDomain, on_delete=models.CASCADE, default='', verbose_name='Sous Domaine')
    text = models.TextField(verbose_name='Texte de la Question')
    can_ask = models.BooleanField(default=True, verbose_name='Est une Question ?')

    def __str__(self):
        return self.text


class Response(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE, related_name='responses')
    answer = models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2')], default=0)

class Questionnaire(models.Model):
    id = models.AutoField(primary_key=True)
    # parent = models.ForeignKey(Parent, on_delete=models.CASCADE, verbose_name='Parent')
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Parent')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Élève',default='')
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE, verbose_name='Formulaire')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')
    date_evaluation = models.DateField(
        verbose_name="Date d'évaluation",
        help_text="Date à laquelle l'évaluation a été réalisée",
        null=True,
        blank=True
    )
    unique_key = models.CharField(max_length=255, unique=False, verbose_name='Clé Unique',default='')

    def __str__(self):
        return f"{self.parent.name} - {self.student.name} - {self.formulaire.title}"

    def save(self, *args, **kwargs):
        # Generate the unique key in the format: "ParentName-StudentName-ddmmyyyy"
        today_date = timezone.now().strftime('%d%m%Y')
        self.unique_key = f"{self.parent.name}-{self.student.name}-{today_date}"
        super().save(*args, **kwargs)

class DomaineResponse(models.Model):
    id = models.AutoField(primary_key=True)
    domaine = models.ForeignKey(Domain, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE, related_name='domaine_responses')
    score_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.domaine.name} - {self.questionnaire} - {self.score_total}"

class SousDomaineResponse(models.Model):
    id = models.AutoField(primary_key=True)
    sous_domaine = models.ForeignKey(SousDomain, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey('Questionnaire', on_delete=models.CASCADE, related_name='sous_domaine_responses')
    score_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sous_domaine.name} - {self.questionnaire} - {self.score_total}"

class AgeTranche(models.Model):
    code = models.CharField(max_length=3)
    label = models.CharField(max_length=100)
    min_months = models.IntegerField()
    max_months = models.IntegerField()

class ScoreParametrage(models.Model):
    tranche = models.ForeignKey(AgeTranche, on_delete=models.CASCADE)
    domain = models.CharField(max_length=50)
    sous_domain = models.CharField(max_length=50)
    score_brut = models.IntegerField()
    ns = models.IntegerField()
    percentile = models.CharField(max_length=10)
    age_developpe = models.CharField(max_length=10)

class AgeDeveloppeParametrage(models.Model):
    sous_domain = models.CharField(max_length=50)  # CVP, LE, etc.
    score_brut = models.IntegerField()
    age_developpe = models.CharField(max_length=10)  # "<12", "13", etc.
    
    def __str__(self):
        return f"{self.sous_domain} - {self.score_brut} - {self.age_developpe}"

    class Meta:
        unique_together = ('sous_domain', 'score_brut')

class NoteStandardPercentile(models.Model):
    DOMAIN_CHOICES = [
        ('Communication', 'Communication'),
        ('Motricité', 'Motricité'),
        ('Comportements', 'Comportements inadaptés')
    ]

    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    somme_score_standard = models.CharField(max_length=10)  # Pour pouvoir stocker "> 61"
    rang_percentile = models.CharField(max_length=10)  # Pour pouvoir stocker "< 1" ou "> 99"

    class Meta:
        unique_together = ('domain', 'somme_score_standard')

    def __str__(self):
        return f"{self.domain} - NS: {self.somme_score_standard} - Percentile: {self.rang_percentile}"

class StudentScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    domain = models.CharField(max_length=50)
    sous_domain = models.CharField(max_length=50)
    score_brut = models.IntegerField()
    ns = models.IntegerField(null=True)
    percentile = models.CharField(max_length=10, null=True)
    niveau = models.CharField(max_length=20, null=True)
    age_developpe = models.CharField(max_length=10, null=True)
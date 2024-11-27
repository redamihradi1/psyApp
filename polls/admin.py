from django.contrib import admin
from .models import Parent, Student, Formulaire, Domain, SousDomain, Question, Questionnaire , Response , DomaineResponse , SousDomaineResponse

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ( 'name','user_name')  # Updated to display user_name instead of user
    list_filter = ('name',)
    search_fields = ('name', 'user_name')  # Search by both name and user_name
    ordering = ('name',)
    
    fieldsets = (
        (None, {'fields': ('user_name', 'name')}),  # Updated field name
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'name')}  # Updated field name
        ),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'age', 'sexe', 'date_of_birth')
    list_filter = ('name', 'age', 'sexe', 'date_of_birth')
    search_fields = ('name',)
    ordering = ('name', 'age', 'sexe', 'date_of_birth')
    fieldsets = (
        (None, {'fields': ('parent', 'name', 'age', 'sexe', 'date_of_birth')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('parent', 'name', 'age', 'sexe', 'date_of_birth')}
        ),
    )

@admin.register(Formulaire)
class FormulaireAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description')
    list_filter = ('title',)
    search_fields = ('title',)
    ordering = ('title',)
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description')}
        ),
    )

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','formulaire')
    list_filter = ('formulaire',)
    search_fields = ('name',)
    ordering = ('formulaire', 'name')
    fieldsets = (
        (None , {'fields': ('formulaire', 'name')}),
    )
    add_fieldsets = (
        ('None', {
            'classes': ('wide',),
            'fields': ('formulaire', 'name')}
        ),
    )

@admin.register(SousDomain)
class SousDomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','domain')
    list_filter = ('domain',)
    search_fields = ('name',)
    ordering = ('domain', 'name')
    fieldsets = (
        (None, {'fields': ('domain', 'name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('domain', 'name')}
        ),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('num_question','sous_domain', 'text','can_ask', )
    list_filter = ('sous_domain','can_ask',)
    search_fields = ('text',)
    ordering = ('sous_domain', 'text')
    fieldsets = (
        (None, {'fields': ('sous_domain', 'text','can_ask', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('sous_domain', 'name','can_ask', )}
        ),
    )

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('unique_key', 'parent', 'student', 'formulaire', 'created_at')
    list_filter = ('parent', 'formulaire', 'created_at')
    search_fields = ('parent__name', 'student__name', 'formulaire__title', 'unique_key')
    ordering = ('created_at',)
    fieldsets = (
        (None, {'fields': ('unique_key','parent', 'student', 'formulaire')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('parent', 'student', 'formulaire', 'unique_key')}
        ),
    )

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin): 

    list_display = ('id','question', 'questionnaire', 'answer')
    list_filter = ('answer',)
    search_fields = ('question__text', 'questionnaire__unique_key', 'answer')
    ordering = ('questionnaire', 'question', 'answer')
    fieldsets = (
        (None, {'fields': ('question', 'questionnaire', 'answer')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('question', 'questionnaire', 'answer')}
        ),
    )


# admin.site.register(DomaineResponse)


@admin.register(DomaineResponse)
class DomaineResponseAdmin(admin.ModelAdmin):
    list_display = ('id','domaine', 'questionnaire', 'score_total')
    list_filter = ('id','domaine', 'questionnaire', 'score_total')
    search_fields = ('id','domaine__name', 'questionnaire__unique_key', 'score_total')
    ordering = ('id','questionnaire', 'domaine', 'score_total')
    fieldsets = (
        ('Domaine reponse infos', {'fields': ('domaine', 'questionnaire', 'score_total')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('domaine', 'questionnaire', 'score_total')}
        ),
    )

@admin.register(SousDomaineResponse)
class SousDomaineResponseAdmin(admin.ModelAdmin):
    list_display = ('id','sous_domaine', 'questionnaire', 'score_total')
    list_filter = ('id','sous_domaine', 'questionnaire', 'score_total')
    search_fields = ('id','sous_domaine__name', 'questionnaire__unique_key', 'score_total')
    ordering = ('id','questionnaire', 'sous_domaine', 'score_total')
    fieldsets = (
        ('Sous domaine reponse infos', {'fields': ('sous_domaine', 'questionnaire', 'score_total')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('sous_domaine', 'questionnaire', 'score_total')}
        ),
    )

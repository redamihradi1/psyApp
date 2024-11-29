from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Parent, Student, Formulaire, Domain, SousDomain, Question, Questionnaire , Response , AgeDeveloppeParametrage,DomaineResponse , SousDomaineResponse ,AgeTranche, ScoreParametrage, StudentScore ,NoteStandardPercentile

# @admin.register(Parent)
# class ParentAdmin(admin.ModelAdmin):
#     list_display = ('username', 'name', 'email')  
#     list_filter = ('name',)
#     search_fields = ('username', 'name', 'email')
#     ordering = ('name',)
    
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'name', 'password1', 'password2')}
#         ),
#     )
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'is_parent', 'is_superuser')
    list_filter = ('name', 'is_parent', 'is_staff', 'is_superuser')
    search_fields = ('username', 'name', 'email')
    ordering = ('name',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email')}),
        ('Permissions', {'fields': ('is_parent', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'password1', 'password2', 'is_parent')}
        ),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'age', 'sexe')
    list_filter = ('parent', 'sexe')
    search_fields = ('name', 'parent__username')

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
    ordering = ('num_question', 'text')
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

@admin.register(AgeTranche)
class AgeTrancheAdmin(admin.ModelAdmin):
    list_display = ('code', 'label', 'min_months', 'max_months')
    search_fields = ('code', 'label')
    ordering = ('min_months', 'max_months')
    fieldsets = (
        (None, {'fields': ('code', 'label', 'min_months', 'max_months')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('code', 'label', 'min_months', 'max_months')}
        ),
    )

@admin.register(ScoreParametrage)
class ScoreParametrageAdmin(admin.ModelAdmin):
    list_display = ('tranche', 'domain', 'sous_domain', 'score_brut', 'ns', 'percentile')
    list_filter = ('tranche', 'domain', 'sous_domain')
    search_fields = ('domain', 'sous_domain')
    ordering = ('tranche', 'domain', 'sous_domain', 'score_brut')
    fieldsets = (
        (None, {'fields': ('tranche', 'domain', 'sous_domain', 'score_brut', 'ns', 'percentile', 'age_developpe')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('tranche', 'domain', 'sous_domain', 'score_brut', 'ns', 'percentile', 'age_developpe')}
        ),
    )

@admin.register(AgeDeveloppeParametrage)
class AgeDeveloppeParametrageAdmin(admin.ModelAdmin):
    list_display = ('sous_domain', 'score_brut', 'age_developpe')
    list_filter = ('sous_domain',)
    search_fields = ('sous_domain', 'score_brut')
    ordering = ('sous_domain', 'score_brut')
    fieldsets = (
        (None, {'fields': ('sous_domain', 'score_brut', 'age_developpe')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('sous_domain', 'score_brut', 'age_developpe')}
        ),
    )


@admin.register(NoteStandardPercentile)
class NoteStandardPercentileAdmin(admin.ModelAdmin):
    list_display = ('domain', 'somme_score_standard', 'rang_percentile')
    list_filter = ('domain',)
    search_fields = ('domain', 'somme_score_standard', 'rang_percentile')
    ordering = ('domain', 'somme_score_standard')
    
    # def has_delete_permission(self, request, obj=None):
    #     # Empêcher la suppression accidentelle des données de référence
    #     return False
        
    # def get_readonly_fields(self, request, obj=None):
    #     # Rendre les champs en lecture seule après création
    #     if obj:  # Si l'objet existe déjà
    #         return ('domain', 'somme_score_standard')
    #     return ()
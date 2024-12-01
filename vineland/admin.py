# vineland/admin.py
from django.contrib import admin
from django.apps import apps
from .models import QuestionVineland, ReponseVineland, PlageItemVineland

class VinelandAdminSite(admin.AdminSite):
    site_header = 'Administration Vineland'
    site_title = 'Vineland Administration'
    index_title = 'Gestion des tests Vineland'

vineland_admin = VinelandAdminSite(name='vineland_admin')

@admin.register(PlageItemVineland)
class PlageItemVinelandAdmin(admin.ModelAdmin):
    list_display = ('sous_domaine', 'item_debut', 'item_fin', 'age_debut', 'age_fin')
    list_filter = ('sous_domaine', 'age_debut')
    search_fields = ('sous_domaine__nom',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sous_domaine')

@admin.register(QuestionVineland)
class QuestionVinelandAdmin(admin.ModelAdmin):
    list_display = ('numero_item', 'sous_domaine', 'texte', 'get_plage_age_display', 'permet_na')
    list_filter = ('sous_domaine', 'permet_na')
    search_fields = ('texte', 'note')
    ordering = ('sous_domaine', 'numero_item')
    fieldsets = (
        ('Informations générales', {
            'fields': ('texte', 'sous_domaine', 'numero_item')
        }),
        ('Paramètres additionnels', {
            'fields': ('note', 'permet_na')
        }),
    )

    def get_plage_age_display(self, obj):
        plage = obj.get_plage_age()
        if plage:
            return str(plage)
        return "Pas de plage d'âge définie"
    get_plage_age_display.short_description = "Plage d'âge"

@admin.register(ReponseVineland)
class ReponseVinelandAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'question', 'reponse', 'created_at')
    list_filter = ('reponse', 'created_at', 'question__sous_domaine')
    search_fields = ('questionnaire__id', 'question__texte')
    raw_id_fields = ('questionnaire', 'question')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('questionnaire', 'question')


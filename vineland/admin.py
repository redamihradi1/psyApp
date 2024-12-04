# vineland/admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.apps import apps
from django.forms import ModelForm
from .models import QuestionVineland, ReponseVineland, PlageItemVineland, EchelleVMapping , NoteDomaineVMapping , IntervaleConfianceSousDomaine , IntervaleConfianceDomaine

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
    list_display = ('reponse', 'question', 'questionnaire', 'created_at')
    list_filter = ('reponse', 'created_at', 'question__sous_domaine')
    search_fields = ('questionnaire__id', 'question__texte')
    raw_id_fields = ('questionnaire', 'question')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('questionnaire', 'question')

@admin.register(EchelleVMapping)
class EchelleVMappingAdmin(admin.ModelAdmin):
   list_display = (
       'sous_domaine',  
       'get_tranche_age',
       'get_note_brute_range',
       'note_echelle_v'
   )
   list_filter = ('sous_domaine', 'note_echelle_v' )
   search_fields = ('sous_domaine__name',)
   ordering = ('sous_domaine', 'age_debut_annee', 'age_debut_mois', 'note_brute_min')

   # Champs regroupés par catégorie dans le formulaire
   fieldsets = (
       ('Sous-domaine', {
           'fields': ('sous_domaine',)
       }),
       ('Tranche d\'âge', {
           'fields': (
               ('age_debut_annee', 'age_debut_mois', 'age_debut_jour'),
               ('age_fin_annee', 'age_fin_mois', 'age_fin_jour')
           )
       }),
       ('Notes', {
           'fields': (
               ('note_brute_min', 'note_brute_max'),
               'note_echelle_v'
           )
       })
   )

   def get_tranche_age(self, obj):
       return f"{obj.age_debut_annee}:{obj.age_debut_mois}:{obj.age_debut_jour} à {obj.age_fin_annee}:{obj.age_fin_mois}:{obj.age_fin_jour}"
   get_tranche_age.short_description = "Tranche d'âge"

   def get_note_brute_range(self, obj):
       return f"{obj.note_brute_min} - {obj.note_brute_max}"
   get_note_brute_range.short_description = "Note brute (min-max)"


class NoteDomaineVMappingForm(ModelForm):
    class Meta:
        model = NoteDomaineVMapping
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        # Vérification des intervalles pour chaque domaine
        domains = [
            ('communication', 'Communication'),
            ('vie_quotidienne', 'Vie quotidienne'),
            ('socialisation', 'Socialisation'),
            ('motricite', 'Motricité')
        ]
        
        for domain_key, domain_name in domains:
            min_val = cleaned_data.get(f'{domain_key}_min')
            max_val = cleaned_data.get(f'{domain_key}_max')
            
            if min_val is not None and max_val is not None:
                if min_val > max_val:
                    raise ValidationError(
                        f"{domain_name}: La valeur minimum ({min_val}) ne peut pas être supérieure "
                        f"à la valeur maximum ({max_val})"
                    )
        
        # Vérification de l'intervalle de la note composite
        comp_min = cleaned_data.get('note_composite_min')
        comp_max = cleaned_data.get('note_composite_max')
        if comp_min and comp_max and comp_min > comp_max:
            raise ValidationError(
                f"Note composite: La valeur minimum ({comp_min}) ne peut pas être supérieure "
                f"à la valeur maximum ({comp_max})"
            )
        
        return cleaned_data

@admin.register(NoteDomaineVMapping)
class NoteDomaineVMappingAdmin(admin.ModelAdmin):
    form = NoteDomaineVMappingForm
    
    list_display = (
        'tranche_age',
        'get_communication_range',
        'get_vie_quotidienne_range',
        'get_socialisation_range',
        'get_motricite_range',
        'note_standard',
        'get_note_composite_range',
        'rang_percentile'
    )
    
    list_filter = ('tranche_age', 'rang_percentile')
    search_fields = ('note_standard', 'rang_percentile')
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('tranche_age', 'note_standard', 'rang_percentile')
        }),
        ('Communication', {
            'fields': (('communication_min', 'communication_max'),)
        }),
        ('Vie quotidienne', {
            'fields': (('vie_quotidienne_min', 'vie_quotidienne_max'),)
        }),
        ('Socialisation', {
            'fields': (('socialisation_min', 'socialisation_max'),)
        }),
        ('Motricité', {
            'fields': (('motricite_min', 'motricite_max'),)
        }),
        ('Note composite', {
            'fields': (('note_composite_min', 'note_composite_max'),)
        }),
    )
    
    def get_communication_range(self, obj):
        if obj.communication_min is not None and obj.communication_max is not None:
            return f"{obj.communication_min}-{obj.communication_max}"
        return "-"
    get_communication_range.short_description = "Communication"
    
    def get_vie_quotidienne_range(self, obj):
        if obj.vie_quotidienne_min is not None and obj.vie_quotidienne_max is not None:
            return f"{obj.vie_quotidienne_min}-{obj.vie_quotidienne_max}"
        return "-"
    get_vie_quotidienne_range.short_description = "Vie quotidienne"
    
    def get_socialisation_range(self, obj):
        if obj.socialisation_min is not None and obj.socialisation_max is not None:
            return f"{obj.socialisation_min}-{obj.socialisation_max}"
        return "-"
    get_socialisation_range.short_description = "Socialisation"
    
    def get_motricite_range(self, obj):
        if obj.motricite_min is not None and obj.motricite_max is not None:
            return f"{obj.motricite_min}-{obj.motricite_max}"
        return "-"
    get_motricite_range.short_description = "Motricité"
    
    def get_note_composite_range(self, obj):
        return f"{obj.note_composite_min}-{obj.note_composite_max}"
    get_note_composite_range.short_description = "Note composite"

@admin.register(IntervaleConfianceSousDomaine)
class IntervaleConfianceSousDomainAdmin(admin.ModelAdmin):
    list_display = (
        'age',
        'niveau_confiance',
        'sous_domaine',
        'format_intervalle',
        'get_domain'
    )
    
    list_filter = (
        'age',
        'niveau_confiance',
        'sous_domaine__domain',
        'sous_domaine',
    )
    
    search_fields = (
        'sous_domaine__name',
        'sous_domaine__domain__name'
    )
    
    ordering = ['age', '-niveau_confiance', 'sous_domaine']
    
    def get_domain(self, obj):
        return obj.sous_domaine.domain.name
    get_domain.short_description = 'Domaine'
    
    def format_intervalle(self, obj):
        return f"±{obj.intervalle}"
    format_intervalle.short_description = 'Intervalle'

    fieldsets = (
        ('Informations générales', {
            'fields': (
                'age',
                'niveau_confiance',
                'sous_domaine',
                'intervalle'
            )
        }),
    )

@admin.register(IntervaleConfianceDomaine)
class IntervaleConfianceDomainAdmin(admin.ModelAdmin):
    list_display = (
        'age',
        'niveau_confiance',
        'domain',
        'format_intervalle',
        'note_composite'
    )
    
    list_filter = (
        'age',
        'niveau_confiance',
        'domain',
    )
    
    search_fields = (
        'domain__name',
    )
    
    ordering = ['age', '-niveau_confiance', 'domain']
    
    def format_intervalle(self, obj):
        return f"±{obj.intervalle}"
    format_intervalle.short_description = 'Intervalle'

    fieldsets = (
        ('Informations générales', {
            'fields': (
                'age',
                'niveau_confiance',
                'domain',
                'intervalle',
            )
        }),
        ('Note composite', {
            'fields': ('note_composite',),
            'classes': ('collapse',),
            'description': 'Note composite de comportement adaptatif (optionnelle)'
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/custom.css',)  # Si vous voulez ajouter des styles personnalisés
        }
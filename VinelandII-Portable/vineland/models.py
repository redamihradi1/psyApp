from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PlageItemVineland(models.Model):
    sous_domaine = models.ForeignKey(
        'polls.SousDomain',  # À remplacer par le nom de votre app
        on_delete=models.CASCADE,
        related_name='plages_items_vineland'
    )
    item_debut = models.PositiveIntegerField(
        verbose_name="Premier item de la plage"
    )
    item_fin = models.PositiveIntegerField(
        verbose_name="Dernier item de la plage"
    )
    age_debut = models.PositiveIntegerField(
        verbose_name="Âge minimum (en années)"
    )
    age_fin = models.PositiveIntegerField(
        verbose_name="Âge maximum (en années)",
        null=True,
        blank=True,
        help_text="Laisser vide si pas de maximum (7+ par exemple)"
    )

    class Meta:
        verbose_name = "Plage d'items Vineland"
        verbose_name_plural = "Plages d'items Vineland"
        ordering = ['sous_domaine', 'item_debut']

    def __str__(self):
        age_str = f"{self.age_debut}-{self.age_fin}" if self.age_fin else f"{self.age_debut}+"
        return f"{self.sous_domaine} - Items {self.item_debut}-{self.item_fin} ({age_str} ans)"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.item_fin < self.item_debut:
            raise ValidationError("Le dernier item doit être supérieur au premier item")

class QuestionVineland(models.Model):
    CHOIX_REPONSES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('NSP', 'Ne sais pas'),
        ('NA', 'Non applicable'),
        ('?', '?'),
        ('', 'Non répondu')
    )

    texte = models.TextField(verbose_name="Question")
    sous_domaine = models.ForeignKey(
        'polls.SousDomain',  # À remplacer par le nom de votre app
        on_delete=models.CASCADE,
        related_name='questions_vineland'
    )
    numero_item = models.PositiveIntegerField(
        verbose_name="Numéro de l'item",
        help_text="Numéro de l'item dans le sous-domaine"
    )
    note = models.TextField(
        verbose_name="Note/Indication", 
        blank=True, 
        null=True,
        help_text="Pour plusieurs lignes, utilisez | comme séparateur"
    )
    permet_na = models.BooleanField(
        verbose_name="Permet la réponse N/A",
        default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Question Vineland"
        verbose_name_plural = "Questions Vineland"
        ordering = ['sous_domaine', 'numero_item']
        unique_together = ['sous_domaine', 'numero_item']

    def __str__(self):
        return f"{self.sous_domaine} - Item {self.numero_item}: {self.texte[:50]}..."
    
    
    def save(self, *args, **kwargs):
        # Nettoyage des notes avant sauvegarde
        if self.note:
            # Remplace les sauts de ligne par le séparateur
            self.note = self.note.replace('\n', '|').replace('\r', '')
        super().save(*args, **kwargs)

    def get_plage_age(self):
        """Retourne la plage d'âge correspondante à cet item"""
        return PlageItemVineland.objects.filter(
            sous_domaine=self.sous_domaine,
            item_debut__lte=self.numero_item,
            item_fin__gte=self.numero_item
        ).first()

class ReponseVineland(models.Model):
    questionnaire = models.ForeignKey(
        'polls.Questionnaire',  # À remplacer par le nom de votre app
        on_delete=models.CASCADE,
        related_name='reponses_vineland'
    )
    question = models.ForeignKey(
        QuestionVineland,
        on_delete=models.CASCADE,
        related_name='reponses'
    )
    reponse = models.CharField(
        max_length=3,
        choices=QuestionVineland.CHOIX_REPONSES,
        null=True,  # Permet des réponses nulles
        blank=True,  # Permet de laisser le champ vide dans les formulaires
        verbose_name="Réponse"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Réponse Vineland"
        verbose_name_plural = "Réponses Vineland"
        unique_together = ['questionnaire', 'question']

    def __str__(self):
        return f"Réponse pour {self.question} - Questionnaire {self.questionnaire.id}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.reponse == 'NA' and not self.question.permet_na:
            raise ValidationError("La réponse 'Non applicable' n'est pas autorisée pour cette question.")
        
class EchelleVMapping(models.Model):
    sous_domaine = models.ForeignKey(
        'polls.SousDomain',
        on_delete=models.CASCADE,
        related_name='echelle_v_mappings',
        verbose_name="Sous-domaine"
    )
    
    # Tranche d'âge
    age_debut_annee = models.PositiveIntegerField(verbose_name="Âge début - Années")
    age_debut_mois = models.PositiveIntegerField(
        verbose_name="Âge début - Mois",
        validators=[MaxValueValidator(11)]
    )
    age_debut_jour = models.PositiveIntegerField(
        verbose_name="Âge début - Jours",
        validators=[MaxValueValidator(30)]
    )
    
    age_fin_annee = models.PositiveIntegerField(verbose_name="Âge fin - Années")
    age_fin_mois = models.PositiveIntegerField(
        verbose_name="Âge fin - Mois",
        validators=[MaxValueValidator(11)]
    )
    age_fin_jour = models.PositiveIntegerField(
        verbose_name="Âge fin - Jours",
        validators=[MaxValueValidator(30)]
    )
    
    # Note brute et correspondance échelle-V
    note_brute_min = models.PositiveIntegerField(verbose_name="Note brute minimum")
    note_brute_max = models.PositiveIntegerField(verbose_name="Note brute maximum")
    note_echelle_v = models.PositiveIntegerField(
        verbose_name="Note échelle-V",
        validators=[MinValueValidator(1), MaxValueValidator(24)]
    )

    class Meta:
        verbose_name = "Correspondance Échelle-V"
        verbose_name_plural = "Correspondances Échelle-V"
        ordering = ['sous_domaine', 'age_debut_annee', 'age_debut_mois', 'note_brute_min']
        constraints = [
            models.CheckConstraint(
                check=models.Q(note_brute_max__gte=models.F('note_brute_min')),
                name='note_brute_max_gte_min'
            ),
            # Contrainte pour s'assurer que l'âge de fin est supérieur à l'âge de début
            models.CheckConstraint(
                check=(
                    models.Q(age_fin_annee__gt=models.F('age_debut_annee')) |
                    (models.Q(age_fin_annee=models.F('age_debut_annee')) & 
                        models.Q(age_fin_mois__gt=models.F('age_debut_mois'))) |
                    (models.Q(age_fin_annee=models.F('age_debut_annee')) & 
                        models.Q(age_fin_mois=models.F('age_debut_mois')) &
                        models.Q(age_fin_jour__gte=models.F('age_debut_jour')))
                ),
                name='age_fin_gte_debut'
            )
        ]

    def __str__(self):
        return (
            f"{self.sous_domaine} - "
            f"{self.age_debut_annee};{self.age_debut_mois};{self.age_debut_jour} à "
            f"{self.age_fin_annee};{self.age_fin_mois};{self.age_fin_jour} - "
            f"Note brute {self.note_brute_min}-{self.note_brute_max} → V : {self.note_echelle_v}"
        )

class NoteDomaineVMapping(models.Model):
    TRANCHES_AGE = [
        ('1-2', '1 à 2 ans'),
        ('3-6', '3 à 6 ans'),
        ('7-18', '7 à 18 ans'),
        ('19-49', '19 à 49 ans'),
        ('50-90', '50 à 90 ans'),
    ]

    # Champs de base
    tranche_age = models.CharField(
        max_length=10,
        choices=TRANCHES_AGE,
        verbose_name="Tranche d'âge"
    )
    
    # Intervalles pour les notes des sous-domaines
    communication_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Communication minimum"
    )
    communication_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Communication maximum"
    )
    
    vie_quotidienne_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Vie quotidienne minimum"
    )
    vie_quotidienne_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Vie quotidienne maximum"
    )
    
    socialisation_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Socialisation minimum"
    )
    socialisation_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Socialisation maximum"
    )
    
    motricite_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Motricité minimum"
    )
    motricite_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(72)],
        verbose_name="Note Motricité maximum"
    )

    # Résultats
    note_standard = models.PositiveIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(160)],
        verbose_name="Note standard"
    )
    note_composite_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Note composite minimum"
    )
    note_composite_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Note composite maximum"
    )
    rang_percentile = models.CharField(
        max_length=10,
        verbose_name="Rang percentile"
    )

    class Meta:
        verbose_name = "Correspondance Note Domaine"
        verbose_name_plural = "Correspondances Notes Domaines"
        # On s'assure qu'il n'y a pas de doublons pour une même combinaison
        unique_together = ['tranche_age', 'note_standard']
        ordering = ['tranche_age', '-note_standard']

    def __str__(self):
        return f"{self.tranche_age} - Note Standard: {self.note_standard} - Rang: {self.rang_percentile}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        errors = {}
        
        # Validation des intervalles
        if self.communication_min and self.communication_max:
            if self.communication_min > self.communication_max:
                errors['communication_min'] = "La note minimum doit être inférieure ou égale à la note maximum"
        
        if self.vie_quotidienne_min and self.vie_quotidienne_max:
            if self.vie_quotidienne_min > self.vie_quotidienne_max:
                errors['vie_quotidienne_min'] = "La note minimum doit être inférieure ou égale à la note maximum"
        
        if self.socialisation_min and self.socialisation_max:
            if self.socialisation_min > self.socialisation_max:
                errors['socialisation_min'] = "La note minimum doit être inférieure ou égale à la note maximum"
        
        if self.motricite_min and self.motricite_max:
            if self.motricite_min > self.motricite_max:
                errors['motricite_min'] = "La note minimum doit être inférieure ou égale à la note maximum"

        if self.note_composite_min > self.note_composite_max:
            errors['note_composite_min'] = "La note composite minimum doit être inférieure ou égale à la note composite maximum"
            
        # Au moins un intervalle de sous-domaine doit être renseigné
        if not any([self.communication_min, self.vie_quotidienne_min, 
                    self.socialisation_min, self.motricite_min]):
            errors['communication_min'] = "Au moins un intervalle de sous-domaine doit être renseigné"
            
        if errors:
            raise ValidationError(errors)
            
    def is_note_in_range(self, domaine, valeur):
        """
        Vérifie si une note d'échelle-V donnée est dans l'intervalle pour un domaine spécifique
        """
        if domaine == 'communication' and self.communication_min and self.communication_max:
            return self.communication_min <= valeur <= self.communication_max
        elif domaine == 'vie_quotidienne' and self.vie_quotidienne_min and self.vie_quotidienne_max:
            return self.vie_quotidienne_min <= valeur <= self.vie_quotidienne_max
        elif domaine == 'socialisation' and self.socialisation_min and self.socialisation_max:
            return self.socialisation_min <= valeur <= self.socialisation_max
        elif domaine == 'motricite' and self.motricite_min and self.motricite_max:
            return self.motricite_min <= valeur <= self.motricite_max
        return False
    
class IntervaleConfianceSousDomaine(models.Model):
    NIVEAUX_CONFIANCE = [
        (95, '95%'),
        (90, '90%'),
        (85, '85%'),
    ]

    TRANCHES_AGE = [
        ('1', '1 an'),
        ('2', '2 ans'),
        ('3', '3 ans'),
        ('4', '4 ans'),
        ('5', '5 ans'),
        ('6', '6 ans'),
        ('7-8', '7-8 ans'),
        ('9-11', '9-11 ans'),
        ('12-14', '12-14 ans'),
        ('15-18', '15-18 ans'),
        ('19-29', '19-29 ans'),
        ('30-49', '30-49 ans'),
        ('50-90', '50-90 ans'),
    ]

    age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    niveau_confiance = models.IntegerField(choices=NIVEAUX_CONFIANCE)
    sous_domaine = models.ForeignKey(
        'polls.SousDomain',
        on_delete=models.CASCADE,
        related_name='intervalles_confiance'
    )
    
    # Intervalle de confiance (±X)
    intervalle = models.IntegerField(
        help_text="Valeur de l'intervalle (ex: ±2 → entrer 2)"
    )

    class Meta:
        verbose_name = "Intervalle de confiance sous-domaine"
        verbose_name_plural = "Intervalles de confiance sous-domaines"
        unique_together = ['age', 'niveau_confiance', 'sous_domaine']
        ordering = ['age', '-niveau_confiance', 'sous_domaine']

    def __str__(self):
        return f"{self.age} - {self.niveau_confiance}% - {self.sous_domaine} (±{self.intervalle})"

class IntervaleConfianceDomaine(models.Model):
    NIVEAUX_CONFIANCE = [
        (95, '95%'),
        (90, '90%'),
        (85, '85%'),
    ]

    TRANCHES_AGE = [
        ('1', '1 an'),
        ('2', '2 ans'),
        ('3', '3 ans'),
        ('4', '4 ans'),
        ('5', '5 ans'),
        ('6', '6 ans'),
        ('7-8', '7-8 ans'),
        ('9-11', '9-11 ans'),
        ('12-14', '12-14 ans'),
        ('15-18', '15-18 ans'),
        ('19-29', '19-29 ans'),
        ('30-49', '30-49 ans'),
        ('50-90', '50-90 ans'),
    ]

    age = models.CharField(max_length=10, choices=TRANCHES_AGE)
    niveau_confiance = models.IntegerField(choices=NIVEAUX_CONFIANCE)
    domain = models.ForeignKey(
        'polls.Domain',
        on_delete=models.CASCADE,
        related_name='intervalles_confiance'
    )
    
    # Intervalle de confiance pour le domaine (±X)
    intervalle = models.IntegerField(
        help_text="Valeur de l'intervalle (ex: ±5 → entrer 5)"
    )
    
    # Note composite de comportement adaptatif
    note_composite = models.IntegerField(
        help_text="Note composite pour ce niveau de confiance",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Intervalle de confiance domaine"
        verbose_name_plural = "Intervalles de confiance domaines"
        unique_together = ['age', 'niveau_confiance', 'domain']
        ordering = ['age', '-niveau_confiance', 'domain']

    def __str__(self):
        base = f"{self.age} - {self.niveau_confiance}% - {self.domain} (±{self.intervalle})"
        if self.note_composite:
            base += f" [Note composite: {self.note_composite}]"
        return base
    
class NiveauAdaptatif(models.Model):
    NIVEAUX = [
        ('faible', 'Faible'),
        ('assez_faible', 'Assez faible'),
        ('adapte', 'Adapté'),
        ('assez_eleve', 'Assez élevé'),
        ('eleve', 'Élevé'),
    ]
    
    niveau = models.CharField(
        max_length=20,
        choices=NIVEAUX,
        verbose_name="Niveau adaptatif"
    )
    echelle_v_min = models.IntegerField(verbose_name="Échelle-v minimum")
    echelle_v_max = models.IntegerField(verbose_name="Échelle-v maximum")
    note_standard_min = models.IntegerField(verbose_name="Note standard minimum")
    note_standard_max = models.IntegerField(verbose_name="Note standard maximum")
    
    class Meta:
        verbose_name = "Niveau adaptatif"
        verbose_name_plural = "Niveaux adaptatifs"
        ordering = ['echelle_v_min']
        
    def __str__(self):
        return f"{self.get_niveau_display()} (Échelle-v: {self.echelle_v_min}-{self.echelle_v_max}, Standard: {self.note_standard_min}-{self.note_standard_max})"

class AgeEquivalentSousDomaine(models.Model):
    SPECIAL_AGES = [
        ('>18', 'Plus de 18 ans'),
        ('<1', 'Moins de 1 an'),
    ]

    sous_domaine = models.ForeignKey(
        'polls.SousDomain',
        on_delete=models.CASCADE,
        verbose_name="Sous-domaine",
        related_name='age_equivalents'
    )
    
    # Pour la note brute
    note_brute_min = models.IntegerField(
        verbose_name="Note brute minimum"
    )
    note_brute_max = models.IntegerField(
        verbose_name="Note brute maximum",
        null=True,
        blank=True
    )
    
    # Pour l'âge équivalent
    age_special = models.CharField(
        max_length=4,
        choices=SPECIAL_AGES,
        null=True,
        blank=True,
        verbose_name="Âge spécial"
    )
    age_annees = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Années"
    )
    age_mois = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Mois",
        validators=[MinValueValidator(0), MaxValueValidator(11)]
    )

    def get_note_brute_display(self):
        if self.note_brute_max:
            return f"{self.note_brute_min}-{self.note_brute_max}"
        return str(self.note_brute_min)

    def get_age_equivalent_display(self):
        if self.age_special:
            if self.age_special == '>18':
                return "Plus de 18 ans"
            return "Moins de 1 an"
        if self.age_annees is not None:
            if self.age_mois:
                return f"{self.age_annees} an(s) et {self.age_mois} mois"
            return str(self.age_annees)
        return "-"

    def __str__(self):
        return f"{self.sous_domaine.name}: {self.get_note_brute_display()} → {self.get_age_equivalent_display()}"

    class Meta:
        verbose_name = "Équivalence d'âge pour sous-domaine"
        verbose_name_plural = "Équivalences d'âge pour sous-domaines"
        ordering = ['sous_domaine', '-age_annees', '-age_mois']
        unique_together = ['sous_domaine', 'note_brute_min', 'note_brute_max']

class ComparaisonDomaineVineland(models.Model):
    """Stocke les valeurs de différence significative pour les comparaisons de domaines (Table D.1)"""
    age = models.CharField(max_length=10)  # Ex: '1', '2', '3-6', '7-8', etc.
    niveau_significativite = models.CharField(max_length=5)  # '.05' ou '.01'
    domaine1 = models.ForeignKey('polls.Domain', on_delete=models.CASCADE, related_name='comparaison_domaine1')
    domaine2 = models.ForeignKey('polls.Domain', on_delete=models.CASCADE, related_name='comparaison_domaine2')
    difference_requise = models.IntegerField()
    
    class Meta:
        unique_together = ('age', 'niveau_significativite', 'domaine1', 'domaine2')
        verbose_name = "Comparaison de domaines"
        verbose_name_plural = "Comparaisons de domaines"
    
    def __str__(self):
        return f"{self.domaine1} vs {self.domaine2} ({self.age} ans, {self.niveau_significativite})"

class ComparaisonSousDomaineVineland(models.Model):
    """Stocke les valeurs de différence significative pour les comparaisons de sous-domaines (Table D.3)"""
    age = models.CharField(max_length=10)  # Ex: '1-2', '3-6', etc.
    niveau_significativite = models.CharField(max_length=5)  # '.05' ou '.01'
    sous_domaine1 = models.ForeignKey('polls.SousDomain', on_delete=models.CASCADE, related_name='comparaison_sous_domaine1')
    sous_domaine2 = models.ForeignKey('polls.SousDomain', on_delete=models.CASCADE, related_name='comparaison_sous_domaine2')
    difference_requise = models.IntegerField()
    
    class Meta:
        unique_together = ('age', 'niveau_significativite', 'sous_domaine1', 'sous_domaine2')
        verbose_name = "Comparaison de sous-domaines"
        verbose_name_plural = "Comparaisons de sous-domaines"
    
    def __str__(self):
        return f"{self.sous_domaine1} vs {self.sous_domaine2} ({self.age} ans, {self.niveau_significativite})"

class FrequenceDifferenceDomaineVineland(models.Model):
    """Stocke les fréquences des différences pour les domaines (Table D.2)"""
    age = models.CharField(max_length=10)
    domaine1 = models.ForeignKey('polls.Domain', on_delete=models.CASCADE, related_name='freq_domaine1')
    domaine2 = models.ForeignKey('polls.Domain', on_delete=models.CASCADE, related_name='freq_domaine2')
    frequence_16 = models.CharField(max_length=10)  # Valeur pour 16% d'occurrence
    frequence_10 = models.CharField(max_length=10)  # Valeur pour 10% d'occurrence
    frequence_5 = models.CharField(max_length=10)   # Valeur pour 5% d'occurrence
    
    class Meta:
        unique_together = ('age', 'domaine1', 'domaine2')
        verbose_name = "Fréquence de différence (domaines)"
        verbose_name_plural = "Fréquences de différence (domaines)"
        
    def __str__(self):
        return f"Fréquence {self.domaine1} vs {self.domaine2} ({self.age} ans)"

class FrequenceDifferenceSousDomaineVineland(models.Model):
    """Stocke les fréquences des différences pour les sous-domaines (Table D.4)"""
    age = models.CharField(max_length=10)
    sous_domaine1 = models.ForeignKey('polls.SousDomain', on_delete=models.CASCADE, related_name='freq_sous_domaine1')
    sous_domaine2 = models.ForeignKey('polls.SousDomain', on_delete=models.CASCADE, related_name='freq_sous_domaine2')
    frequence_16 = models.CharField(max_length=10)  # Valeur pour 16% d'occurrence
    frequence_10 = models.CharField(max_length=10)  # Valeur pour 10% d'occurrence
    frequence_5 = models.CharField(max_length=10)   # Valeur pour 5% d'occurrence
    
    class Meta:
        unique_together = ('age', 'sous_domaine1', 'sous_domaine2')
        verbose_name = "Fréquence de différence (sous-domaines)"
        verbose_name_plural = "Fréquences de différence (sous-domaines)"
        
    def __str__(self):
        return f"Fréquence {self.sous_domaine1} vs {self.sous_domaine2} ({self.age} ans)"
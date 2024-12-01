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
        (0, '0'),
        (1, '1'),
        (2, '2'),
        ('NSP', 'Ne sais pas'),
        ('NA', 'Non applicable')
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
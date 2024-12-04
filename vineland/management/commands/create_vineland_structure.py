from django.core.management.base import BaseCommand
from polls.models import Formulaire, Domain, SousDomain

class Command(BaseCommand):
    help = 'Création de la structure Vineland (formulaire, domaines et sous-domaines)'

    def handle(self, *args, **options):
        self.stdout.write('Création de la structure Vineland...')

        try:
            # Création du formulaire Vineland
            formulaire, created = Formulaire.objects.get_or_create(
                title='Vineland',
                defaults={
                    'description': 'Échelles de comportement adaptatif de Vineland (Vineland-II)'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('Formulaire Vineland créé'))

            # Structure des domaines et sous-domaines
            structures = {
                'Communication': [
                    'Réceptive',
                    'Expressive',
                    'Écrite'
                ],
                'Vie quotidienne': [
                    'Personnelle',
                    'Domestique',
                    'Communautaire'
                ],
                'Socialisation': [
                    'Relations interpersonnelles',
                    'Jeu et temps libre',
                    'Adaptation'
                ],
                'Motricité': [
                    'Globale',
                    'Fine'
                ],
                'Comportements problématiques': [
                    'Section A',
                    'Section B',
                    'Section C',
                    'Section D'
                ]
            }

            for domaine_nom, sous_domaines in structures.items():
                domaine, created = Domain.objects.get_or_create(
                    name=domaine_nom,
                    formulaire=formulaire
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Domaine créé : {domaine_nom}'))
                
                for sous_domaine_nom in sous_domaines:
                    sous_domaine, created = SousDomain.objects.get_or_create(
                        name=sous_domaine_nom,
                        domain=domaine
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Sous-domaine créé : {sous_domaine_nom}'))

            self.stdout.write(self.style.SUCCESS('Structure Vineland créée avec succès !'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la création : {str(e)}'))
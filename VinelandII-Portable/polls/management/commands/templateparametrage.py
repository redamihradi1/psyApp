from django.core.management.base import BaseCommand
from ...models import AgeTranche, ScoreParametrage
import json

class Command(BaseCommand):
    help = 'Import parametrage data for tranche deuxAnsCinqMoisATroisAns from JSON files'

    def handle(self, *args, **options):
        # Création ou récupération de la tranche d'âge
        tranche, created = AgeTranche.objects.get_or_create(
            code='',
            defaults={
                'label': '',
                'min_months':,
                'max_months':
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Tranche créée: {tranche.label}'))

        # Charger les données JSON
        json_data = {
            "CVP": [],
            "LE": [...],   
            "LR": [...],   
            "MF": [...],
            "MG": [...],
            "IOM": [...],
            "EA": [...],
            "RS": [...],
            "CMC": [...],
            "CVC": [...],
        }
        
        count = 0

        for domain, items in json_data.items():
            for item in items:
                note_brute = item['noteBrute']
                ns = item.get('ns', '-')
                percentile = item.get('percentile', '-')
                
                if ns != '-':
                    ScoreParametrage.objects.get_or_create(
                        tranche=tranche,
                        domain='Performance',
                        sous_domain=domain,
                        score_brut=int(note_brute),
                        defaults={
                            'ns': int(ns),
                            'percentile': percentile
                        }
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} paramètres créés pour {tranche.label}'))

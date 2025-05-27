from django.core.management.base import BaseCommand
from django.db import transaction
from polls.models import SousDomain
from vineland.models import EchelleVMapping
import pandas as pd
import os
from collections import defaultdict
from tabulate import tabulate
import time

class Command(BaseCommand):
    help = 'Importe les données de la grille d\'évaluation depuis un fichier Excel'

    COLONNES_MAPPING = {
        'Réceptive': 1,
        'Expressive': 2,
        'Écrite': 3,
        'Personnelle': 4,
        'Domestique': 5,
        'Communautaire': 6,
        'Relations interpersonnelles': 7,
        'Jeu et temps libre': 8,
        'Adaptation': 9,
        'Globale': 10,
        'Fine': 11
    }

    EXCEL_TO_DB_MAPPING = {
        'Réceptif': 'Réceptive',
        'Expressif': 'Expressive',
        'Écrit': 'Écrite',
        'Personnel': 'Personnelle',
        'Domestique': 'Domestique',
        'Communauté': 'Communautaire',
        'Relations interpersonnelles': 'Relations interpersonnelles',
        'Jeu et temps libre': 'Jeu et temps libre',
        'Adaptation': 'Adaptation',
        'Motricité globale': 'Globale',
        'Motricité fine': 'Fine'
    }

    def __init__(self):
        super().__init__()
        self.stats = {
            'start_time': None,
            'end_time': None,
            'total_sheets': 0,
            'processed_sheets': 0,
            'failed_sheets': 0,
            'valid_data_cells': 0,  # Nouveau compteur pour les données valides
            'successful_imports': 0,
            'failed_imports': 0,
            'errors_by_type': defaultdict(int),
            'stats_by_domain': defaultdict(lambda: {
                'successful': 0,
                'failed': 0,
                'total': 0
            }),
            'sheets_details': defaultdict(lambda: {
                'successful': 0,
                'failed': 0,
                'total': 0,
                'valid_cells': 0,  # Nouveau compteur par feuille
                'errors': []
            })
        }

    def parse_sheet_name(self, sheet_name):
        try:
            sheet_name = str(sheet_name)
            if not sheet_name or sheet_name.lower().startswith('sheet'):
                return None

            start, end = sheet_name.replace(':', '.').split('-')
            start_parts = start.split('.')
            end_parts = end.split('.')

            # Construction du dictionnaire avec gestion des jours
            result = {
                'age_debut_annee': int(float(start_parts[0])),
                'age_debut_mois': int(float(start_parts[1])) if len(start_parts) > 1 else 0,
                'age_debut_jour': int(float(start_parts[2])) if len(start_parts) > 2 else (0 if len(start_parts) == 2 else int(float(start_parts[1]))),
                'age_fin_annee': int(float(end_parts[0])),
                'age_fin_mois': int(float(end_parts[1])) if len(end_parts) > 1 else 0,
                'age_fin_jour': int(float(end_parts[2])) if len(end_parts) > 2 else (0 if len(end_parts) == 2 else int(float(end_parts[1])))
            }

            # Debug pour voir les valeurs
            self.stdout.write(f"Parsing {sheet_name} -> {result}")
            
            return result

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Erreur de parsing du nom de feuille "{sheet_name}": {str(e)}')
            )
            return None

    def parse_note_brute(self, note, sheet_name='', row_index=None):
        if pd.isna(note) or note == '-' or note == '':
            return None

        note = str(note).strip()

        if note in self.EXCEL_TO_DB_MAPPING:
            return None
        
        if '-' in note:
            try:
                parts = note.split('-')
                min_val = int(float(parts[0].strip()))
                max_val = int(float(parts[1].strip()))
                
                if min_val > max_val:
                    min_val, max_val = max_val, min_val
                
                return min_val, max_val
                
            except Exception as e:
                return None

        try:
            val = int(float(note))
            return val, val
        except:
            return None

    def print_stats(self):
        self.stats['end_time'] = time.time()
        execution_time = self.stats['end_time'] - self.stats['start_time']

        self.stdout.write("\n" + "="*50)
        self.stdout.write("RAPPORT D'IMPORTATION DÉTAILLÉ")
        self.stdout.write("="*50 + "\n")

        general_stats = [
            ["Durée d'exécution", f"{execution_time:.2f} secondes"],
            ["Feuilles traitées", f"{self.stats['processed_sheets']}/{self.stats['total_sheets']}"],
            ["Feuilles échouées", self.stats['failed_sheets']],
            ["Données valides trouvées", self.stats['valid_data_cells']],
            ["Imports réussis", self.stats['successful_imports']],
            ["Imports échoués", self.stats['failed_imports']],
            ["Taux de réussite réel", f"{(self.stats['successful_imports']/max(self.stats['valid_data_cells'], 1))*100:.2f}%"]
        ]
        self.stdout.write("\n1. STATISTIQUES GÉNÉRALES:")
        self.stdout.write(tabulate(general_stats, tablefmt="grid"))

        domain_stats = []
        for domain, data in self.stats['stats_by_domain'].items():
            success_rate = (data['successful'] / max(data['total'], 1)) * 100
            domain_stats.append([
                domain,
                data['successful'],
                data['failed'],
                data['total'],
                f"{success_rate:.2f}%"
            ])

        self.stdout.write("\n2. STATISTIQUES PAR SOUS-DOMAINE:")
        self.stdout.write(tabulate(
            sorted(domain_stats, key=lambda x: x[0]),
            headers=["Sous-domaine", "Réussis", "Échoués", "Total", "Taux de réussite"],
            tablefmt="grid"
        ))

        sheet_stats = []
        for sheet_name, data in sorted(self.stats['sheets_details'].items()):
            if data['total'] > 0:
                success_rate = (data['successful'] / max(data['valid_cells'], 1)) * 100
                error_summary = ', '.join(set(data['errors'][:3]))
                sheet_stats.append([
                    sheet_name,
                    data['successful'],
                    data['failed'],
                    data['valid_cells'],
                    f"{success_rate:.2f}%",
                    error_summary[:100] + '...' if len(error_summary) > 100 else error_summary
                ])

        self.stdout.write("\n3. STATISTIQUES PAR FEUILLE:")
        self.stdout.write(tabulate(
            sheet_stats,
            headers=["Feuille", "Réussis", "Échoués", "Données valides", "Taux", "Erreurs principales"],
            tablefmt="grid"
        ))

        if self.stats['errors_by_type']:
            error_stats = sorted(
                [[error, count] for error, count in self.stats['errors_by_type'].items()],
                key=lambda x: x[1], 
                reverse=True
            )
            self.stdout.write("\n4. RÉSUMÉ DES ERREURS:")
            self.stdout.write(tabulate(
                error_stats,
                headers=["Type d'erreur", "Occurrences"],
                tablefmt="grid"
            ))

    @transaction.atomic
    def handle(self, *args, **options):
        self.stats['start_time'] = time.time()
        
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        excel_path = os.path.join(desktop_path, 'grille_evaluation.xlsx')

        if not os.path.exists(excel_path):
            self.stderr.write(self.style.ERROR(f'Fichier Excel non trouvé: {excel_path}'))
            return

        self.stdout.write(self.style.SUCCESS('Début de l\'importation...'))
        self.stdout.write('Suppression des anciennes données...')
        EchelleVMapping.objects.all().delete()

        excel = pd.ExcelFile(excel_path)
        self.stats['total_sheets'] = len(excel.sheet_names)

        for sheet_name in excel.sheet_names:
            try:
                self.stdout.write(f'Traitement de la feuille: {sheet_name}')
                age_info = self.parse_sheet_name(sheet_name)
                if not age_info:
                    self.stats['failed_sheets'] += 1
                    self.stats['sheets_details'][sheet_name]['errors'].append("Erreur de parsing du nom")
                    continue

                df = pd.read_excel(excel, sheet_name=sheet_name)
                
                # Trouver l'index de la première ligne de données
                start_index = 0
                for idx, row in df.iterrows():
                    if not pd.isna(row.iloc[0]) and str(row.iloc[0]).isdigit():
                        start_index = idx
                        break
                
                # Prendre seulement les lignes à partir de l'index trouvé
                df = df.iloc[start_index:].reset_index(drop=True)
                
                self.stats['processed_sheets'] += 1

                for excel_nom, db_nom in self.EXCEL_TO_DB_MAPPING.items():
                    try:
                        colonne_index = self.COLONNES_MAPPING[db_nom]
                        sous_domaine = SousDomain.objects.get(name=db_nom)
                        
                        for index, row in df.iterrows():
                            try:
                                note_echelle_v = row.iloc[0]
                                if pd.isna(note_echelle_v):
                                    continue

                                note_brute = self.parse_note_brute(row.iloc[colonne_index], sheet_name, index + 1)
                                if note_brute is None:
                                    continue

                                # Incrémenter le compteur de données valides
                                self.stats['valid_data_cells'] += 1
                                self.stats['sheets_details'][sheet_name]['valid_cells'] += 1

                                min_val, max_val = note_brute
                                
                                EchelleVMapping.objects.create(
                                    sous_domaine=sous_domaine,
                                    **age_info,
                                    note_brute_min=min_val,
                                    note_brute_max=max_val,
                                    note_echelle_v=int(float(note_echelle_v))
                                )
                                self.stats['successful_imports'] += 1
                                self.stats['stats_by_domain'][db_nom]['successful'] += 1
                                self.stats['stats_by_domain'][db_nom]['total'] += 1
                                self.stats['sheets_details'][sheet_name]['successful'] += 1
                                self.stats['sheets_details'][sheet_name]['total'] += 1

                            except Exception as e:
                                error_type = type(e).__name__
                                error_msg = f"{error_type} à la ligne {index + 3}: {str(e)}"
                                self.stats['errors_by_type'][error_type] += 1
                                self.stats['failed_imports'] += 1
                                self.stats['stats_by_domain'][db_nom]['failed'] += 1
                                self.stats['stats_by_domain'][db_nom]['total'] += 1
                                self.stats['sheets_details'][sheet_name]['failed'] += 1
                                self.stats['sheets_details'][sheet_name]['total'] += 1
                                self.stats['sheets_details'][sheet_name]['errors'].append(error_msg)

                    except SousDomain.DoesNotExist:
                        error_msg = f"Sous-domaine non trouvé: {db_nom}"
                        self.stats['errors_by_type']['SousDomainNotFound'] += 1
                        self.stats['sheets_details'][sheet_name]['errors'].append(error_msg)
                        self.stderr.write(self.style.WARNING(error_msg))

            except Exception as e:
                self.stats['failed_sheets'] += 1
                error_type = type(e).__name__
                error_msg = f"{error_type}: {str(e)}"
                self.stats['errors_by_type'][error_type] += 1
                self.stats['sheets_details'][sheet_name]['errors'].append(error_msg)
                self.stderr.write(self.style.ERROR(f'Erreur lors du traitement de la feuille {sheet_name}: {error_msg}'))

        self.print_stats()
        self.stdout.write(self.style.SUCCESS('\nImport terminé avec succès'))
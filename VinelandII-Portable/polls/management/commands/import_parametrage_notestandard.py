from django.core.management.base import BaseCommand
from ...models import NoteStandardPercentile

class Command(BaseCommand):
    help = 'Import percentile data for note standard calculations'

    def handle(self, *args, **options):
        # Données pour la Communication
        ns_cat_communication = [
    {"sommeScoreStandard": "3", "rangPercentile": "<1"},
    {"sommeScoreStandard": "4", "rangPercentile": "<1"},
    {"sommeScoreStandard": "5", "rangPercentile": "<1"},
    {"sommeScoreStandard": "6", "rangPercentile": "<1"},
    {"sommeScoreStandard": "7", "rangPercentile": "<1"},
    {"sommeScoreStandard": "8", "rangPercentile": "<1"},
    {"sommeScoreStandard": "9", "rangPercentile": "<1"},
    {"sommeScoreStandard": "10", "rangPercentile": "<1"},
    {"sommeScoreStandard": "11", "rangPercentile": "<1"},
    {"sommeScoreStandard": "12", "rangPercentile": "1"},
    {"sommeScoreStandard": "13", "rangPercentile": "1"},
    {"sommeScoreStandard": "14", "rangPercentile": "2"},
    {"sommeScoreStandard": "15", "rangPercentile": "3"},
    {"sommeScoreStandard": "16", "rangPercentile": "4"},
    {"sommeScoreStandard": "17", "rangPercentile": "6"},
    {"sommeScoreStandard": "18", "rangPercentile": "7"},
    {"sommeScoreStandard": "19", "rangPercentile": "11"},
    {"sommeScoreStandard": "20", "rangPercentile": "14"},
    {"sommeScoreStandard": "21", "rangPercentile": "18"},
    {"sommeScoreStandard": "22", "rangPercentile": "23"},
    {"sommeScoreStandard": "23", "rangPercentile": "26"},
    {"sommeScoreStandard": "24", "rangPercentile": "28"},
    {"sommeScoreStandard": "25", "rangPercentile": "31"},
    {"sommeScoreStandard": "26", "rangPercentile": "34"},
    {"sommeScoreStandard": "27", "rangPercentile": "36"},
    {"sommeScoreStandard": "28", "rangPercentile": "38"},
    {"sommeScoreStandard": "29", "rangPercentile": "40"},
    {"sommeScoreStandard": "30", "rangPercentile": "43"},
    {"sommeScoreStandard": "31", "rangPercentile": "46"},
    {"sommeScoreStandard": "32", "rangPercentile": "50"},
    {"sommeScoreStandard": "33", "rangPercentile": "55"},
    {"sommeScoreStandard": "34", "rangPercentile": "59"},
    {"sommeScoreStandard": "35", "rangPercentile": "64"},
    {"sommeScoreStandard": "36", "rangPercentile": "68"},
    {"sommeScoreStandard": "37", "rangPercentile": "71"},
    {"sommeScoreStandard": "38", "rangPercentile": "75"},
    {"sommeScoreStandard": "39", "rangPercentile": "77"},
    {"sommeScoreStandard": "40", "rangPercentile": "80"},
    {"sommeScoreStandard": "41", "rangPercentile": "82"},
    {"sommeScoreStandard": "42", "rangPercentile": "85"},
    {"sommeScoreStandard": "43", "rangPercentile": "88"},
    {"sommeScoreStandard": "44", "rangPercentile": "91"},
    {"sommeScoreStandard": "45", "rangPercentile": "94"},
    {"sommeScoreStandard": "46", "rangPercentile": "96"},
    {"sommeScoreStandard": "47", "rangPercentile": "97"},
    {"sommeScoreStandard": "48", "rangPercentile": "98"},
    {"sommeScoreStandard": "49", "rangPercentile": "99"},
    {"sommeScoreStandard": ">49", "rangPercentile": ">99"},


]

        # Données pour la Motricité
        ns_cat_moteur = [
    {"sommeScoreStandard": "3", "rangPercentile": "<1"},
    {"sommeScoreStandard": "4", "rangPercentile": "<1"},
    {"sommeScoreStandard": "5", "rangPercentile": "<1"},
    {"sommeScoreStandard": "6", "rangPercentile": "1"},
    {"sommeScoreStandard": "7", "rangPercentile": "1"},
    {"sommeScoreStandard": "8", "rangPercentile": "2"},
    {"sommeScoreStandard": "9", "rangPercentile": "2"},
    {"sommeScoreStandard": "10", "rangPercentile": "2"},
    {"sommeScoreStandard": "11", "rangPercentile": "3"},
    {"sommeScoreStandard": "12", "rangPercentile": "5"},
    {"sommeScoreStandard": "13", "rangPercentile": "5"},
    {"sommeScoreStandard": "14", "rangPercentile": "6"},
    {"sommeScoreStandard": "15", "rangPercentile": "6"},
    {"sommeScoreStandard": "16", "rangPercentile": "7"},
    {"sommeScoreStandard": "17", "rangPercentile": "8"},
    {"sommeScoreStandard": "18", "rangPercentile": "10"},
    {"sommeScoreStandard": "19", "rangPercentile": "13"},
    {"sommeScoreStandard": "20", "rangPercentile": "15"},
    {"sommeScoreStandard": "21", "rangPercentile": "16"},
    {"sommeScoreStandard": "22", "rangPercentile": "19"},
    {"sommeScoreStandard": "23", "rangPercentile": "21"},
    {"sommeScoreStandard": "24", "rangPercentile": "24"},
    {"sommeScoreStandard": "25", "rangPercentile": "27"},
    {"sommeScoreStandard": "26", "rangPercentile": "29"},
    {"sommeScoreStandard": "27", "rangPercentile": "31"},
    {"sommeScoreStandard": "28", "rangPercentile": "33"},
    {"sommeScoreStandard": "29", "rangPercentile": "37"},
    {"sommeScoreStandard": "30", "rangPercentile": "40"},
    {"sommeScoreStandard": "31", "rangPercentile": "43"},
    {"sommeScoreStandard": "32", "rangPercentile": "46"},
    {"sommeScoreStandard": "33", "rangPercentile": "51"},
    {"sommeScoreStandard": "34", "rangPercentile": "57"},
    {"sommeScoreStandard": "35", "rangPercentile": "64"},
    {"sommeScoreStandard": "36", "rangPercentile": "69"},
    {"sommeScoreStandard": "37", "rangPercentile": "75"},
    {"sommeScoreStandard": "38", "rangPercentile": "81"},
    {"sommeScoreStandard": "39", "rangPercentile": "88"},
    {"sommeScoreStandard": "40", "rangPercentile": "92"},
    {"sommeScoreStandard": "41", "rangPercentile": "96"},
    {"sommeScoreStandard": "42", "rangPercentile": "98"},
    {"sommeScoreStandard": ">42", "rangPercentile": ">99"}
]

        # Données pour les Comportements
        ns_cat_comportement = [
    {"sommeScoreStandard": "4", "rangPercentile": "<1"},
    {"sommeScoreStandard": "5", "rangPercentile": "<1"},
    {"sommeScoreStandard": "6", "rangPercentile": "<1"},
    {"sommeScoreStandard": "7", "rangPercentile": "<1"},
    {"sommeScoreStandard": "8", "rangPercentile": "<1"},
    {"sommeScoreStandard": "9", "rangPercentile": "<1"},
    {"sommeScoreStandard": "10", "rangPercentile": "<1"},
    {"sommeScoreStandard": "11", "rangPercentile": "<1"},
    {"sommeScoreStandard": "12", "rangPercentile": "<1"},
    {"sommeScoreStandard": "13", "rangPercentile": "<1"},
    {"sommeScoreStandard": "14", "rangPercentile": "<1"},
    {"sommeScoreStandard": "15", "rangPercentile": "1"},
    {"sommeScoreStandard": "16", "rangPercentile": "1"},
    {"sommeScoreStandard": "17", "rangPercentile": "3"},
    {"sommeScoreStandard": "18", "rangPercentile": "4"},
    {"sommeScoreStandard": "19", "rangPercentile": "4"},
    {"sommeScoreStandard": "20", "rangPercentile": "4"},
    {"sommeScoreStandard": "21", "rangPercentile": "4"},
    {"sommeScoreStandard": "22", "rangPercentile": "4"},
    {"sommeScoreStandard": "23", "rangPercentile": "4"},
    {"sommeScoreStandard": "24", "rangPercentile": "5"},
    {"sommeScoreStandard": "25", "rangPercentile": "6"},
    {"sommeScoreStandard": "26", "rangPercentile": "6"},
    {"sommeScoreStandard": "27", "rangPercentile": "7"},
    {"sommeScoreStandard": "28", "rangPercentile": "7"},
    {"sommeScoreStandard": "29", "rangPercentile": "8"},
    {"sommeScoreStandard": "30", "rangPercentile": "9"},
    {"sommeScoreStandard": "31", "rangPercentile": "10"},
    {"sommeScoreStandard": "32", "rangPercentile": "10"},
    {"sommeScoreStandard": "33", "rangPercentile": "11"},
    {"sommeScoreStandard": "34", "rangPercentile": "15"},
    {"sommeScoreStandard": "35", "rangPercentile": "19"},
    {"sommeScoreStandard": "36", "rangPercentile": "21"},
    {"sommeScoreStandard": "37", "rangPercentile": "24"},
    {"sommeScoreStandard": "38", "rangPercentile": "27"},
    {"sommeScoreStandard": "39", "rangPercentile": "31"},
    {"sommeScoreStandard": "40", "rangPercentile": "37"},
    {"sommeScoreStandard": "41", "rangPercentile": "41"},
    {"sommeScoreStandard": "42", "rangPercentile": "46"},
    {"sommeScoreStandard": "43", "rangPercentile": "49"},
    {"sommeScoreStandard": "44", "rangPercentile": "50"},
    {"sommeScoreStandard": "45", "rangPercentile": "52"},
    {"sommeScoreStandard": "46", "rangPercentile": "57"},
    {"sommeScoreStandard": "47", "rangPercentile": "63"},
    {"sommeScoreStandard": "48", "rangPercentile": "69"},
    {"sommeScoreStandard": "49", "rangPercentile": "75"},
    {"sommeScoreStandard": "50", "rangPercentile": "79"},
    {"sommeScoreStandard": "51", "rangPercentile": "83"},
    {"sommeScoreStandard": "52", "rangPercentile": "84"},
    {"sommeScoreStandard": "53", "rangPercentile": "87"},
    {"sommeScoreStandard": "54", "rangPercentile": "89"},
    {"sommeScoreStandard": "55", "rangPercentile": "91"},
    {"sommeScoreStandard": "56", "rangPercentile": "94"},
    {"sommeScoreStandard": "57", "rangPercentile": "97"},
    {"sommeScoreStandard": "58", "rangPercentile": "98"},
    {"sommeScoreStandard": "59", "rangPercentile": "99"},
    {"sommeScoreStandard": "60", "rangPercentile": "99"},
    {"sommeScoreStandard": "61", "rangPercentile": "99"},
    {"sommeScoreStandard": ">61", "rangPercentile": ">99"}
]

        data_mapping = {
            'Communication': ns_cat_communication,
            'Motricité': ns_cat_moteur,
            'Comportements': ns_cat_comportement
        }

        count = 0
        for domain, data_list in data_mapping.items():
            for item in data_list:
                
                NoteStandardPercentile.objects.get_or_create(
                    domain=domain,
                    somme_score_standard=str(item['sommeScoreStandard']),
                    defaults={
                        'rang_percentile': item['rangPercentile']
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} paramètres de percentile créés'))

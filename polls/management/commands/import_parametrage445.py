from django.core.management.base import BaseCommand
from ...models import AgeTranche, ScoreParametrage
import json

class Command(BaseCommand):
    help = 'Import parametrage data for tranche deuxAnsCinqMoisATroisAns from JSON files'

    def handle(self, *args, **options):
        # Création ou récupération de la tranche d'âge
        tranche, created = AgeTranche.objects.get_or_create(
            code='445',
            defaults={
                'label': '4 ans à 4 ans 5 mois',
                'min_months': 48,
                'max_months': 57
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Tranche créée: {tranche.label}'))

        # Charger les données JSON
        json_data = {
            "CVP": [
    {"noteBrute": "0", "ns": "4", "percentile": "<4"},
    {"noteBrute": "1", "ns": "4", "percentile": "<4"},
    {"noteBrute": "2", "ns": "4", "percentile": "<4"},
    {"noteBrute": "3", "ns": "5", "percentile": "4"},
    {"noteBrute": "4", "ns": "5", "percentile": "4"},
    {"noteBrute": "5", "ns": "5", "percentile": "4"},
    {"noteBrute": "6", "ns": "5", "percentile": "4"},
    {"noteBrute": "7", "ns": "5", "percentile": "4"},
    {"noteBrute": "8", "ns": "6", "percentile": "13"},
    {"noteBrute": "9", "ns": "6", "percentile": "13"},
    {"noteBrute": "10", "ns": "6", "percentile": "13"},
    {"noteBrute": "11", "ns": "6", "percentile": "13"},
    {"noteBrute": "12", "ns": "6", "percentile": "13"},
    {"noteBrute": "13", "ns": "6", "percentile": "13"},
    {"noteBrute": "14", "ns": "7", "percentile": "26"},
    {"noteBrute": "15", "ns": "7", "percentile": "26"},
    {"noteBrute": "16", "ns": "7", "percentile": "26"},
    {"noteBrute": "17", "ns": "7", "percentile": "26"},
    {"noteBrute": "18", "ns": "7", "percentile": "26"},
    {"noteBrute": "19", "ns": "8", "percentile": "41"},
    {"noteBrute": "20", "ns": "8", "percentile": "41"},
    {"noteBrute": "21", "ns": "8", "percentile": "41"},
    {"noteBrute": "22", "ns": "8", "percentile": "41"},
    {"noteBrute": "23", "ns": "8", "percentile": "41"},
    {"noteBrute": "24", "ns": "9", "percentile": "52"},
    {"noteBrute": "25", "ns": "9", "percentile": "52"},
    {"noteBrute": "26", "ns": "9", "percentile": "52"},
    {"noteBrute": "27", "ns": "9", "percentile": "52"},
    {"noteBrute": "28", "ns": "9", "percentile": "52"},
    {"noteBrute": "29", "ns": "9", "percentile": "52"},
    {"noteBrute": "30", "ns": "10", "percentile": "56"},
    {"noteBrute": "31", "ns": "10", "percentile": "56"},
    {"noteBrute": "32", "ns": "10", "percentile": "56"},
    {"noteBrute": "33", "ns": "11", "percentile": "59"},
    {"noteBrute": "34", "ns": "11", "percentile": "59"},
    {"noteBrute": "35", "ns": "11", "percentile": "59"},
    {"noteBrute": "36", "ns": "11", "percentile": "59"},
    {"noteBrute": "37", "ns": "12", "percentile": "69"},
    {"noteBrute": "38", "ns": "12", "percentile": "69"},
    {"noteBrute": "39", "ns": "12", "percentile": "69"},
    {"noteBrute": "40", "ns": "12", "percentile": "69"},
    {"noteBrute": "41", "ns": "13", "percentile": "76"},
    {"noteBrute": "42", "ns": "13", "percentile": "76"},
    {"noteBrute": "43", "ns": "13", "percentile": "76"},
    {"noteBrute": "44", "ns": "13", "percentile": "76"},
    {"noteBrute": "45", "ns": "13", "percentile": "76"},
    {"noteBrute": "46", "ns": "14", "percentile": "83"},
    {"noteBrute": "47", "ns": "14", "percentile": "83"},
    {"noteBrute": "48", "ns": "14", "percentile": "83"},
    {"noteBrute": "49", "ns": "14", "percentile": "83"},
    {"noteBrute": "50", "ns": "14", "percentile": "83"},
    {"noteBrute": "51", "ns": "14", "percentile": "83"},
    {"noteBrute": "52", "ns": "15", "percentile": "89"},
    {"noteBrute": "53", "ns": "15", "percentile": "89"},
    {"noteBrute": "54", "ns": "15", "percentile": "89"},
    {"noteBrute": "55", "ns": "15", "percentile": "89"},
    {"noteBrute": "56", "ns": "16", "percentile": "89"},
    {"noteBrute": "57", "ns": "16", "percentile": "89"},
    {"noteBrute": "58", "ns": "16", "percentile": "89"},
    {"noteBrute": "59", "ns": "16", "percentile": "89"},
    {"noteBrute": "60", "ns": "17", "percentile": "94"},
    {"noteBrute": "61", "ns": "17", "percentile": "94"},
    {"noteBrute": "62", "ns": "17", "percentile": "94"},
    {"noteBrute": "63", "ns": "17", "percentile": "94"},
    {"noteBrute": "64", "ns": "17", "percentile": "94"},
    {"noteBrute": "65", "ns": "18", "percentile": ">99"},
    {"noteBrute": "66", "ns": "18", "percentile": ">99"},
    {"noteBrute": "67", "ns": "18", "percentile": ">99"},
    {"noteBrute": "68", "ns": "18", "percentile": ">99"}
],
            "LE": [
    {"noteBrute": "0", "ns": "6", "percentile": "13"},
    {"noteBrute": "1", "ns": "6", "percentile": "13"},
    {"noteBrute": "2", "ns": "7", "percentile": "28"},
    {"noteBrute": "3", "ns": "7", "percentile": "28"},
    {"noteBrute": "4", "ns": "7", "percentile": "28"},
    {"noteBrute": "5", "ns": "8", "percentile": "33"},
    {"noteBrute": "6", "ns": "8", "percentile": "33"},
    {"noteBrute": "7", "ns": "8", "percentile": "33"},
    {"noteBrute": "8", "ns": "8", "percentile": "33"},
    {"noteBrute": "9", "ns": "9", "percentile": "43"},
    {"noteBrute": "10", "ns": "9", "percentile": "43"},
    {"noteBrute": "11", "ns": "9", "percentile": "43"},
    {"noteBrute": "12", "ns": "9", "percentile": "43"},
    {"noteBrute": "13", "ns": "9", "percentile": "43"},
    {"noteBrute": "14", "ns": "10", "percentile": "55"},
    {"noteBrute": "15", "ns": "10", "percentile": "55"},
    {"noteBrute": "16", "ns": "10", "percentile": "55"},
    {"noteBrute": "17", "ns": "10", "percentile": "55"},
    {"noteBrute": "18", "ns": "11", "percentile": "63"},
    {"noteBrute": "19", "ns": "11", "percentile": "63"},
    {"noteBrute": "20", "ns": "11", "percentile": "63"},
    {"noteBrute": "21", "ns": "12", "percentile": "68"},
    {"noteBrute": "22", "ns": "12", "percentile": "68"},
    {"noteBrute": "23", "ns": "12", "percentile": "68"},
    {"noteBrute": "24", "ns": "12", "percentile": "68"},
    {"noteBrute": "25", "ns": "13", "percentile": "70"},
    {"noteBrute": "26", "ns": "13", "percentile": "70"},
    {"noteBrute": "27", "ns": "13", "percentile": "70"},
    {"noteBrute": "28", "ns": "13", "percentile": "70"},
    {"noteBrute": "29", "ns": "13", "percentile": "70"},
    {"noteBrute": "30", "ns": "14", "percentile": "75"},
    {"noteBrute": "31", "ns": "14", "percentile": "75"},
    {"noteBrute": "32", "ns": "14", "percentile": "75"},
    {"noteBrute": "33", "ns": "14", "percentile": "75"},
    {"noteBrute": "34", "ns": "15", "percentile": "85"},
    {"noteBrute": "35", "ns": "15", "percentile": "85"},
    {"noteBrute": "36", "ns": "15", "percentile": "85"},
    {"noteBrute": "37", "ns": "15", "percentile": "85"},
    {"noteBrute": "38", "ns": "16", "percentile": "95"},
    {"noteBrute": "39", "ns": "16", "percentile": "95"},
    {"noteBrute": "40", "ns": "16", "percentile": "95"},
    {"noteBrute": "41", "ns": "17", "percentile": ">99"},
    {"noteBrute": "42", "ns": "17", "percentile": ">99"},
    {"noteBrute": "43", "ns": "17", "percentile": ">99"},
    {"noteBrute": "44", "ns": "17", "percentile": ">99"},
    {"noteBrute": "45", "ns": "18", "percentile": ">99"},
    {"noteBrute": "46", "ns": "18", "percentile": ">99"},
    {"noteBrute": "47", "ns": "18", "percentile": ">99"},
    {"noteBrute": "48", "ns": "19", "percentile": ">99"},
    {"noteBrute": "49", "ns": "19", "percentile": ">99"},
    {"noteBrute": "50", "ns": "19", "percentile": ">99"}
],   
            "LR": [
    {"noteBrute": "0", "ns": "6", "percentile": "13"},
    {"noteBrute": "1", "ns": "6", "percentile": "13"},
    {"noteBrute": "2", "ns": "6", "percentile": "13"},
    {"noteBrute": "3", "ns": "6", "percentile": "13"},
    {"noteBrute": "4", "ns": "7", "percentile": "31"},
    {"noteBrute": "5", "ns": "7", "percentile": "31"},
    {"noteBrute": "6", "ns": "7", "percentile": "31"},
    {"noteBrute": "7", "ns": "8", "percentile": "40"},
    {"noteBrute": "8", "ns": "8", "percentile": "40"},
    {"noteBrute": "9", "ns": "8", "percentile": "40"},
    {"noteBrute": "10", "ns": "8", "percentile": "40"},
    {"noteBrute": "11", "ns": "9", "percentile": "48"},
    {"noteBrute": "12", "ns": "9", "percentile": "48"},
    {"noteBrute": "13", "ns": "9", "percentile": "48"},
    {"noteBrute": "14", "ns": "9", "percentile": "48"},
    {"noteBrute": "15", "ns": "10", "percentile": "52"},
    {"noteBrute": "16", "ns": "10", "percentile": "52"},
    {"noteBrute": "17", "ns": "10", "percentile": "52"},
    {"noteBrute": "18", "ns": "10", "percentile": "52"},
    {"noteBrute": "19", "ns": "11", "percentile": "54"},
    {"noteBrute": "20", "ns": "11", "percentile": "54"},
    {"noteBrute": "21", "ns": "11", "percentile": "54"},
    {"noteBrute": "22", "ns": "11", "percentile": "54"},
    {"noteBrute": "23", "ns": "12", "percentile": "63"},
    {"noteBrute": "24", "ns": "12", "percentile": "63"},
    {"noteBrute": "25", "ns": "12", "percentile": "63"},
    {"noteBrute": "26", "ns": "12", "percentile": "63"},
    {"noteBrute": "27", "ns": "13", "percentile": "75"},
    {"noteBrute": "28", "ns": "13", "percentile": "75"},
    {"noteBrute": "29", "ns": "13", "percentile": "75"},
    {"noteBrute": "30", "ns": "14", "percentile": "81"},
    {"noteBrute": "31", "ns": "14", "percentile": "81"},
    {"noteBrute": "32", "ns": "14", "percentile": "81"},
    {"noteBrute": "33", "ns": "14", "percentile": "81"},
    {"noteBrute": "34", "ns": "15", "percentile": "88"},
    {"noteBrute": "35", "ns": "15", "percentile": "88"},
    {"noteBrute": "36", "ns": "15", "percentile": "88"},
    {"noteBrute": "37", "ns": "16", "percentile": "96"},
    {"noteBrute": "38", "ns": "16", "percentile": "96"}
],   
            "MF": [
    {"noteBrute": "0", "ns": "1", "percentile": "2"},
    {"noteBrute": "1", "ns": "1", "percentile": "2"},
    {"noteBrute": "2", "ns": "1", "percentile": "2"},
    {"noteBrute": "3", "ns": "1", "percentile": "2"},
    {"noteBrute": "4", "ns": "1", "percentile": "2"},
    {"noteBrute": "5", "ns": "1", "percentile": "2"},
    {"noteBrute": "6", "ns": "2", "percentile": "4"},
    {"noteBrute": "7", "ns": "2", "percentile": "4"},
    {"noteBrute": "8", "ns": "2", "percentile": "4"},
    {"noteBrute": "9", "ns": "3", "percentile": "4"},
    {"noteBrute": "10", "ns": "3", "percentile": "4"},
    {"noteBrute": "11", "ns": "4", "percentile": "7"},
    {"noteBrute": "12", "ns": "4", "percentile": "7"},
    {"noteBrute": "13", "ns": "4", "percentile": "7"},
    {"noteBrute": "14", "ns": "5", "percentile": "11"},
    {"noteBrute": "15", "ns": "5", "percentile": "11"},
    {"noteBrute": "16", "ns": "5", "percentile": "11"},
    {"noteBrute": "17", "ns": "6", "percentile": "15"},
    {"noteBrute": "18", "ns": "6", "percentile": "15"},
    {"noteBrute": "19", "ns": "7", "percentile": "26"},
    {"noteBrute": "20", "ns": "7", "percentile": "26"},
    {"noteBrute": "21", "ns": "7", "percentile": "26"},
    {"noteBrute": "22", "ns": "8", "percentile": "35"},
    {"noteBrute": "23", "ns": "8", "percentile": "35"},
    {"noteBrute": "24", "ns": "8", "percentile": "35"},
    {"noteBrute": "25", "ns": "9", "percentile": "46"},
    {"noteBrute": "26", "ns": "9", "percentile": "46"},
    {"noteBrute": "27", "ns": "9", "percentile": "46"},
    {"noteBrute": "28", "ns": "10", "percentile": "57"},
    {"noteBrute": "29", "ns": "10", "percentile": "57"},
    {"noteBrute": "30", "ns": "11", "percentile": "59"},
    {"noteBrute": "31", "ns": "11", "percentile": "59"},
    {"noteBrute": "32", "ns": "11", "percentile": "59"},
    {"noteBrute": "33", "ns": "12", "percentile": "69"},
    {"noteBrute": "34", "ns": "12", "percentile": "69"},
    {"noteBrute": "35", "ns": "12", "percentile": "69"},
    {"noteBrute": "36", "ns": "13", "percentile": "81"},
    {"noteBrute": "37", "ns": "13", "percentile": "81"},
    {"noteBrute": "38", "ns": "14", "percentile": "93"},
    {"noteBrute": "39", "ns": "14", "percentile": "93"},
    {"noteBrute": "40", "ns": "15", "percentile": ">99"}
],
            "MG": [
    {"noteBrute": "0", "ns": "1", "percentile": "<2"},
    {"noteBrute": "1", "ns": "2", "percentile": "<2"},
    {"noteBrute": "2", "ns": "2", "percentile": "<2"},
    {"noteBrute": "3", "ns": "2", "percentile": "<2"},
    {"noteBrute": "4", "ns": "3", "percentile": "2"},
    {"noteBrute": "5", "ns": "3", "percentile": "2"},
    {"noteBrute": "6", "ns": "3", "percentile": "2"},
    {"noteBrute": "7", "ns": "4", "percentile": "6"},
    {"noteBrute": "8", "ns": "4", "percentile": "6"},
    {"noteBrute": "9", "ns": "5", "percentile": "9"},
    {"noteBrute": "10", "ns": "5", "percentile": "9"},
    {"noteBrute": "11", "ns": "5", "percentile": "9"},
    {"noteBrute": "12", "ns": "5", "percentile": "9"},
    {"noteBrute": "13", "ns": "6", "percentile": "13"},
    {"noteBrute": "14", "ns": "6", "percentile": "13"},
    {"noteBrute": "15", "ns": "7", "percentile": "20"},
    {"noteBrute": "16", "ns": "7", "percentile": "20"},
    {"noteBrute": "17", "ns": "8", "percentile": "33"},
    {"noteBrute": "18", "ns": "8", "percentile": "33"},
    {"noteBrute": "19", "ns": "9", "percentile": "46"},
    {"noteBrute": "20", "ns": "9", "percentile": "46"},
    {"noteBrute": "21", "ns": "9", "percentile": "46"},
    {"noteBrute": "22", "ns": "10", "percentile": "56"},
    {"noteBrute": "23", "ns": "10", "percentile": "56"},
    {"noteBrute": "24", "ns": "11", "percentile": "59"},
    {"noteBrute": "25", "ns": "11", "percentile": "59"},
    {"noteBrute": "26", "ns": "12", "percentile": "65"},
    {"noteBrute": "27", "ns": "12", "percentile": "65"},
    {"noteBrute": "28", "ns": "13", "percentile": "80"},
    {"noteBrute": "29", "ns": "13", "percentile": "80"},
    {"noteBrute": "30", "ns": "14", "percentile": "94"}
],
            "IOM": [
    {"noteBrute": "0", "ns": "4", "percentile": "6"},
    {"noteBrute": "1", "ns": "4", "percentile": "6"},
    {"noteBrute": "2", "ns": "5", "percentile": "17"},
    {"noteBrute": "3", "ns": "5", "percentile": "17"},
    {"noteBrute": "4", "ns": "6", "percentile": "22"},
    {"noteBrute": "5", "ns": "6", "percentile": "22"},
    {"noteBrute": "6", "ns": "7", "percentile": "28"},
    {"noteBrute": "7", "ns": "8", "percentile": "39"},
    {"noteBrute": "8", "ns": "8", "percentile": "39"},
    {"noteBrute": "9", "ns": "9", "percentile": "46"},
    {"noteBrute": "10", "ns": "9", "percentile": "46"},
    {"noteBrute": "11", "ns": "10", "percentile": "50"},
    {"noteBrute": "12", "ns": "10", "percentile": "50"},
    {"noteBrute": "13", "ns": "11", "percentile": "59"},
    {"noteBrute": "14", "ns": "11", "percentile": "59"},
    {"noteBrute": "15", "ns": "12", "percentile": "69"},
    {"noteBrute": "16", "ns": "12", "percentile": "69"},
    {"noteBrute": "17", "ns": "13", "percentile": "74"},
    {"noteBrute": "18", "ns": "13", "percentile": "74"},
    {"noteBrute": "19", "ns": "14", "percentile": "89"},
    {"noteBrute": "20", "ns": "14", "percentile": "89"}
],
            "EA": [
    {"noteBrute": "0", "ns": "5", "percentile": "2"},
    {"noteBrute": "1", "ns": "5", "percentile": "2"},
    {"noteBrute": "2", "ns": "6", "percentile": "6"},
    {"noteBrute": "3", "ns": "6", "percentile": "6"},
    {"noteBrute": "4", "ns": "7", "percentile": "15"},
    {"noteBrute": "5", "ns": "7", "percentile": "15"},
    {"noteBrute": "6", "ns": "8", "percentile": "25"},
    {"noteBrute": "7", "ns": "8", "percentile": "25"},
    {"noteBrute": "8", "ns": "8", "percentile": "25"},
    {"noteBrute": "9", "ns": "9", "percentile": "35"},
    {"noteBrute": "10", "ns": "9", "percentile": "35"},
    {"noteBrute": "11", "ns": "10", "percentile": "45"},
    {"noteBrute": "12", "ns": "10", "percentile": "45"},
    {"noteBrute": "13", "ns": "11", "percentile": "58"},
    {"noteBrute": "14", "ns": "11", "percentile": "58"},
    {"noteBrute": "15", "ns": "12", "percentile": "68"},
    {"noteBrute": "16", "ns": "12", "percentile": "68"},
    {"noteBrute": "17", "ns": "13", "percentile": "81"},
    {"noteBrute": "18", "ns": "13", "percentile": "81"},
    {"noteBrute": "19", "ns": "14", "percentile": "91"},
    {"noteBrute": "20", "ns": "14", "percentile": "91"},
    {"noteBrute": "21", "ns": "15", "percentile": "97"},
    {"noteBrute": "22", "ns": "15", "percentile": "97"}
],
            "RS": [
    {"noteBrute": "0", "ns": "5", "percentile": "3"},
    {"noteBrute": "1", "ns": "5", "percentile": "3"},
    {"noteBrute": "2", "ns": "6", "percentile": "9"},
    {"noteBrute": "3", "ns": "6", "percentile": "9"},
    {"noteBrute": "4", "ns": "7", "percentile": "17"},
    {"noteBrute": "5", "ns": "7", "percentile": "17"},
    {"noteBrute": "6", "ns": "7", "percentile": "17"},
    {"noteBrute": "7", "ns": "8", "percentile": "28"},
    {"noteBrute": "8", "ns": "8", "percentile": "28"},
    {"noteBrute": "9", "ns": "9", "percentile": "41"},
    {"noteBrute": "10", "ns": "9", "percentile": "41"},
    {"noteBrute": "11", "ns": "10", "percentile": "50"},
    {"noteBrute": "12", "ns": "10", "percentile": "50"},
    {"noteBrute": "13", "ns": "11", "percentile": "59"},
    {"noteBrute": "14", "ns": "11", "percentile": "59"},
    {"noteBrute": "15", "ns": "12", "percentile": "73"},
    {"noteBrute": "16", "ns": "12", "percentile": "73"},
    {"noteBrute": "17", "ns": "12", "percentile": "73"},
    {"noteBrute": "18", "ns": "13", "percentile": "86"},
    {"noteBrute": "19", "ns": "13", "percentile": "86"},
    {"noteBrute": "20", "ns": "13", "percentile": "86"},
    {"noteBrute": "21", "ns": "14", "percentile": "93"},
    {"noteBrute": "22", "ns": "14", "percentile": "93"},
    {"noteBrute": "23", "ns": "15", "percentile": "98"},
    {"noteBrute": "24", "ns": "15", "percentile": "98"}
],
            "CMC": [
    {"noteBrute": "0", "ns": "1", "percentile": "<2"},
    {"noteBrute": "1", "ns": "2", "percentile": "2"},
    {"noteBrute": "2", "ns": "2", "percentile": "2"},
    {"noteBrute": "3", "ns": "2", "percentile": "2"},
    {"noteBrute": "4", "ns": "3", "percentile": "4"},
    {"noteBrute": "5", "ns": "3", "percentile": "4"},
    {"noteBrute": "6", "ns": "4", "percentile": "6"},
    {"noteBrute": "7", "ns": "4", "percentile": "6"},
    {"noteBrute": "8", "ns": "5", "percentile": "8"},
    {"noteBrute": "9", "ns": "5", "percentile": "8"},
    {"noteBrute": "10", "ns": "6", "percentile": "10"},
    {"noteBrute": "11", "ns": "6", "percentile": "10"},
    {"noteBrute": "12", "ns": "7", "percentile": "17"},
    {"noteBrute": "13", "ns": "7", "percentile": "17"},
    {"noteBrute": "14", "ns": "8", "percentile": "33"},
    {"noteBrute": "15", "ns": "8", "percentile": "33"},
    {"noteBrute": "16", "ns": "8", "percentile": "33"},
    {"noteBrute": "17", "ns": "8", "percentile": "33"},
    {"noteBrute": "18", "ns": "9", "percentile": "42"},
    {"noteBrute": "19", "ns": "9", "percentile": "42"},
    {"noteBrute": "20", "ns": "10", "percentile": "46"},
    {"noteBrute": "21", "ns": "10", "percentile": "46"},
    {"noteBrute": "22", "ns": "11", "percentile": "58"},
    {"noteBrute": "23", "ns": "11", "percentile": "58"},
    {"noteBrute": "24", "ns": "12", "percentile": "67"},
    {"noteBrute": "25", "ns": "12", "percentile": "67"},
    {"noteBrute": "26", "ns": "13", "percentile": "75"},
    {"noteBrute": "27", "ns": "13", "percentile": "75"},
    {"noteBrute": "28", "ns": "14", "percentile": "88"},
    {"noteBrute": "29", "ns": "14", "percentile": "88"},
    {"noteBrute": "30", "ns": "15", "percentile": "88"}
],
            "CVC": [
    {"noteBrute": "0", "ns": "3", "percentile": "8"},
    {"noteBrute": "1", "ns": "3", "percentile": "8"},
    {"noteBrute": "2", "ns": "4", "percentile": "15"},
    {"noteBrute": "3", "ns": "4", "percentile": "15"},
    {"noteBrute": "4", "ns": "5", "percentile": "15"},
    {"noteBrute": "5", "ns": "5", "percentile": "15"},
    {"noteBrute": "6", "ns": "6", "percentile": "15"},
    {"noteBrute": "7", "ns": "7", "percentile": "23"},
    {"noteBrute": "8", "ns": "7", "percentile": "23"},
    {"noteBrute": "9", "ns": "8", "percentile": "31"},
    {"noteBrute": "10", "ns": "8", "percentile": "31"},
    {"noteBrute": "11", "ns": "9", "percentile": "35"},
    {"noteBrute": "12", "ns": "10", "percentile": "38"},
    {"noteBrute": "13", "ns": "10", "percentile": "38"},
    {"noteBrute": "14", "ns": "11", "percentile": "46"},
    {"noteBrute": "15", "ns": "11", "percentile": "46"},
    {"noteBrute": "16", "ns": "12", "percentile": "62"},
    {"noteBrute": "17", "ns": "12", "percentile": "62"},
    {"noteBrute": "18", "ns": "13", "percentile": "73"},
    {"noteBrute": "19", "ns": "14", "percentile": "85"},
    {"noteBrute": "20", "ns": "14", "percentile": "85"},
    {"noteBrute": "21", "ns": "15", "percentile": "96"},
    {"noteBrute": "22", "ns": "15", "percentile": "96"}
],
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

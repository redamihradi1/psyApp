"""
Script pour importer un test Vineland depuis JSON
Usage: python import_vineland_test.py <fichier.json>
"""

import os
import sys
import django
import json
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from polls.models import Student, Questionnaire, Question, SousDomain, Domain, Formulaire
from vineland.models import ReponseVineland, QuestionVineland
from django.contrib.auth import get_user_model

User = get_user_model()


def import_test_vineland(json_file):
    """Importe un test Vineland depuis un fichier JSON"""
    
    # Lire le fichier JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier introuvable : {json_file}")
        return False
    except json.JSONDecodeError:
        print(f"❌ Fichier JSON invalide : {json_file}")
        return False
    
    print(f"📁 Importation depuis : {json_file}")
    print(f"📅 Exporté le : {data['export_date']}")
    
    # 1. Récupérer le premier parent (User) disponible
    premier_parent = User.objects.first()
    if not premier_parent:
        print("❌ Aucun utilisateur trouvé dans la base. Créez d'abord un utilisateur.")
        return False
    
    print(f"  ℹ️  Parent utilisé : {premier_parent.username}")
    
    # 2. Créer ou récupérer le patient (Student)
    patient_data = data['patient']
    print(f"\n👤 Patient : {patient_data['prenom']} {patient_data['nom']}")
    
    # Essayer de trouver un patient existant
    try:
        student = Student.objects.get(
            name=f"{patient_data['prenom']} {patient_data['nom']}",
            date_of_birth=patient_data['date_naissance']
        )
        print(f"  ℹ️  Patient existant trouvé : {student.name}")
    except Student.DoesNotExist:
        # Créer le patient avec le premier parent
        student = Student.objects.create(
            name=f"{patient_data['prenom']} {patient_data['nom']}",
            date_of_birth=patient_data['date_naissance'],
            parent=premier_parent
        )
        print(f"  ✅ Patient créé : {student.name}")
    
    # 3. Récupérer le formulaire Vineland
    try:
        formulaire = Formulaire.objects.get(title__icontains='Vineland')
        print(f"  ✅ Formulaire trouvé : {formulaire.title}")
    except Formulaire.DoesNotExist:
        print("  ❌ Formulaire Vineland introuvable")
        print("  📝 Formulaires disponibles :")
        for form in Formulaire.objects.all():
            print(f"     - {form.title}")
        return False
    
    # 4. Créer le questionnaire
    test_data = data['test']
    date_passation_str = test_data['date_passation']
    
    # Nettoyer la date (enlever les millisecondes et le timezone)
    if '.' in date_passation_str:
        date_passation_str = date_passation_str.split('.')[0]
    if '+' in date_passation_str:
        date_passation_str = date_passation_str.split('+')[0]
    
    date_passation = datetime.fromisoformat(date_passation_str)
    
    questionnaire = Questionnaire.objects.create(
        student=student,
        parent=premier_parent,
        formulaire=formulaire,
        created_at=date_passation,
    )
    
    print(f"\n📋 Questionnaire créé : ID {questionnaire.id}")
    print(f"  📅 Date : {date_passation}")
    
    # 5. Importer les réponses
    reponses_importees = 0
    reponses_erreurs = 0
    erreurs_details = []
    
    print(f"\n📝 Import des {len(data['reponses'])} réponses...")
    
    for reponse_data in data['reponses']:
        try:
            # Trouver le domaine
            domain = Domain.objects.get(
                name=reponse_data['domaine'],
                formulaire=formulaire
            )
            
            # Trouver le sous-domaine
            sous_domaine = SousDomain.objects.get(
                name=reponse_data['sous_domaine'],
                domain=domain
            )
            
            # Trouver la question Vineland
            question = QuestionVineland.objects.get(
                sous_domaine=sous_domaine,
                numero_item=reponse_data['numero_item']
            )
            
            # Créer la réponse Vineland
            ReponseVineland.objects.create(
                question=question,
                questionnaire=questionnaire,
                reponse=reponse_data['reponse']
            )
            
            reponses_importees += 1
            
            if reponses_importees % 50 == 0:
                print(f"  ⏳ {reponses_importees} réponses importées...")
            
        except Exception as e:
            reponses_erreurs += 1
            erreur_msg = f"{reponse_data['domaine']} > {reponse_data['sous_domaine']} > Item {reponse_data['numero_item']}: {str(e)}"
            erreurs_details.append(erreur_msg)
            
            if reponses_erreurs <= 5:
                print(f"  ⚠️  Erreur: {erreur_msg}")
    
    # 6. Résumé
    print(f"\n{'='*60}")
    print(f"✅ IMPORT TERMINÉ")
    print(f"{'='*60}")
    print(f"  🎯 Questionnaire ID : {questionnaire.id}")
    print(f"  👤 Patient : {student.name}")
    print(f"  ✅ Réponses importées : {reponses_importees}")
    print(f"  ❌ Réponses en erreur : {reponses_erreurs}")
    
    if reponses_erreurs > 5:
        print(f"  📝 Voir le fichier error_log.txt pour tous les détails")
        with open('error_log.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(erreurs_details))
    
    print(f"{'='*60}")
    print(f"\n🔗 URL pour voir les résultats :")
    print(f"   http://127.0.0.1:8000/vineland/{questionnaire.id}/scores/")
    
    return True


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python import_vineland_test.py <fichier.json>")
        print("Exemple: python import_vineland_test.py vineland_test_1_export_20251018.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if import_test_vineland(json_file):
        print("\n🎉 Import réussi ! Vous pouvez maintenant comparer les résultats.")
    else:
        print("\n❌ Import échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(1)
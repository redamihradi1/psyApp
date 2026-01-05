# export_vineland_config.py
import os
import sys
import django
import json

# Ajouter le répertoire du projet au path Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Import des modèles depuis polls (Domain, SousDomain)
from polls.models import Domain, SousDomain, Formulaire

# Import des modèles depuis vineland
from vineland.models import (
    QuestionVineland,
    PlageItemVineland,
    EchelleVMapping,
    NoteDomaineVMapping,
    IntervaleConfianceSousDomaine,
    IntervaleConfianceDomaine,
    NiveauAdaptatif,
    AgeEquivalentSousDomaine,
    ComparaisonDomaineVineland,
    ComparaisonSousDomaineVineland,
    FrequenceDifferenceDomaineVineland,
    FrequenceDifferenceSousDomaineVineland
)

def choose_formulaire():
    """Permet à l'utilisateur de choisir quel formulaire exporter"""
    print("\n" + "="*60)
    print("🎯 EXPORT DE CONFIGURATION - CHOIX DU FORMULAIRE")
    print("="*60)
    
    formulaires = Formulaire.objects.all()
    
    if not formulaires.exists():
        print("❌ Aucun formulaire trouvé dans la base de données !")
        return None
    
    print("\n📋 Formulaires disponibles :")
    for i, form in enumerate(formulaires, 1):
        print(f"   {i}. {form.title} - {form.description}")
    
    print(f"   0. Exporter TOUS les formulaires")
    
    while True:
        try:
            choice = input("\n👉 Votre choix (0-{}): ".format(len(formulaires)))
            choice = int(choice)
            
            if choice == 0:
                print("\n✅ Export de TOUS les formulaires sélectionné")
                return None  # None = tous les formulaires
            elif 1 <= choice <= len(formulaires):
                selected = list(formulaires)[choice - 1]
                print(f"\n✅ Formulaire sélectionné : {selected.title}")
                return selected
            else:
                print(f"❌ Veuillez entrer un nombre entre 0 et {len(formulaires)}")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide")
        except KeyboardInterrupt:
            print("\n\n❌ Export annulé par l'utilisateur")
            sys.exit(0)


def export_data(formulaire_filter=None):
    """
    Export les données de configuration
    
    Args:
        formulaire_filter: Formulaire spécifique à exporter, ou None pour tous
    """
    data = {
        'formulaires': [],
        'domains': [],
        'sous_domains': [],
        'questions': [],
        'plages_items': [],
        'echelle_v_mappings': [],
        'note_domaine_mappings': [],
        'intervalles_confiance_sous_domaine': [],
        'intervalles_confiance_domaine': [],
        'niveaux_adaptatifs': [],
        'ages_equivalents': [],
        'comparaisons_domaines': [],
        'comparaisons_sous_domaines': [],
        'frequences_domaines': [],
        'frequences_sous_domaines': []
    }
    
    print("\n" + "="*60)
    print("📦 DÉBUT DE L'EXPORT")
    print("="*60 + "\n")
    
    # Export Formulaires
    print("📋 Export des formulaires...")
    formulaire_map = {}
    formulaires_query = Formulaire.objects.all()
    if formulaire_filter:
        formulaires_query = formulaires_query.filter(id=formulaire_filter.id)
    
    for formulaire in formulaires_query:
        formulaire_data = {
            'id': formulaire.id,
            'title': formulaire.title,
            'description': formulaire.description
        }
        data['formulaires'].append(formulaire_data)
        formulaire_map[formulaire.id] = formulaire.title
    
    # Export Domaines
    print("📁 Export des domaines...")
    domain_map = {}
    domains_query = Domain.objects.all()
    if formulaire_filter:
        domains_query = domains_query.filter(formulaire_id=formulaire_filter.id)
    
    for domain in domains_query:
        domain_data = {
            'id': domain.id,
            'formulaire_title': formulaire_map.get(domain.formulaire_id, ''),
            'name': domain.name
        }
        data['domains'].append(domain_data)
        domain_map[domain.id] = domain.name
    
    # Récupérer les IDs des domaines filtrés
    domain_ids = list(domain_map.keys())
    
    # Export Sous-Domaines
    print("📂 Export des sous-domaines...")
    sous_domain_map = {}
    sous_domains_query = SousDomain.objects.filter(domain_id__in=domain_ids) if domain_ids else SousDomain.objects.none()
    
    for sous_domain in sous_domains_query:
        sous_domain_data = {
            'id': sous_domain.id,
            'domain_name': domain_map.get(sous_domain.domain_id, ''),
            'name': sous_domain.name
        }
        data['sous_domains'].append(sous_domain_data)
        sous_domain_map[sous_domain.id] = sous_domain.name
    
    sous_domain_ids = list(sous_domain_map.keys())
    
    # Export Questions
    print("❓ Export des questions...")
    questions_query = QuestionVineland.objects.filter(sous_domaine_id__in=sous_domain_ids) if sous_domain_ids else QuestionVineland.objects.none()
    for question in questions_query:
        data['questions'].append({
            'sous_domaine_name': sous_domain_map.get(question.sous_domaine_id, ''),
            'numero_item': question.numero_item,
            'texte': question.texte,
            'note': question.note or '',
            'permet_na': question.permet_na
        })
    
    # Export Plages d'items
    print("📊 Export des plages d'items...")
    plages_query = PlageItemVineland.objects.filter(sous_domaine_id__in=sous_domain_ids) if sous_domain_ids else PlageItemVineland.objects.none()
    for plage in plages_query:
        data['plages_items'].append({
            'sous_domaine_name': sous_domain_map.get(plage.sous_domaine_id, ''),
            'item_debut': plage.item_debut,
            'item_fin': plage.item_fin,
            'age_debut': plage.age_debut,
            'age_fin': plage.age_fin
        })
    
    # Export Échelle-V Mappings
    print("📈 Export des mappings échelle-V...")
    mappings_query = EchelleVMapping.objects.filter(sous_domaine_id__in=sous_domain_ids) if sous_domain_ids else EchelleVMapping.objects.none()
    for mapping in mappings_query:
        data['echelle_v_mappings'].append({
            'sous_domaine_name': sous_domain_map.get(mapping.sous_domaine_id, ''),
            'age_debut_annee': mapping.age_debut_annee,
            'age_debut_mois': mapping.age_debut_mois,
            'age_debut_jour': mapping.age_debut_jour if hasattr(mapping, 'age_debut_jour') else 0,
            'age_fin_annee': mapping.age_fin_annee,
            'age_fin_mois': mapping.age_fin_mois,
            'age_fin_jour': mapping.age_fin_jour if hasattr(mapping, 'age_fin_jour') else 0,
            'note_brute_min': mapping.note_brute_min,
            'note_brute_max': mapping.note_brute_max,
            'note_echelle_v': mapping.note_echelle_v
        })
    
    # Export Note Domaine Mappings
    print("🎯 Export des mappings notes domaines...")
    for mapping in NoteDomaineVMapping.objects.all():
        data['note_domaine_mappings'].append({
            'tranche_age': mapping.tranche_age,
            'communication_min': mapping.communication_min,
            'communication_max': mapping.communication_max,
            'vie_quotidienne_min': mapping.vie_quotidienne_min,
            'vie_quotidienne_max': mapping.vie_quotidienne_max,
            'socialisation_min': mapping.socialisation_min,
            'socialisation_max': mapping.socialisation_max,
            'motricite_min': mapping.motricite_min,
            'motricite_max': mapping.motricite_max,
            'note_standard': mapping.note_standard,
            'note_composite_min': mapping.note_composite_min,
            'note_composite_max': mapping.note_composite_max,
            'rang_percentile': mapping.rang_percentile
        })
    
    # Export Intervalles Confiance Sous-Domaine
    print("📏 Export des intervalles de confiance (sous-domaines)...")
    intervalles_sd_query = IntervaleConfianceSousDomaine.objects.filter(sous_domaine_id__in=sous_domain_ids) if sous_domain_ids else IntervaleConfianceSousDomaine.objects.none()
    for intervalle in intervalles_sd_query:
        data['intervalles_confiance_sous_domaine'].append({
            'age': intervalle.age,
            'niveau_confiance': intervalle.niveau_confiance,
            'sous_domaine_name': sous_domain_map.get(intervalle.sous_domaine_id, ''),
            'intervalle': intervalle.intervalle
        })
    
    # Export Intervalles Confiance Domaine
    print("📐 Export des intervalles de confiance (domaines)...")
    intervalles_d_query = IntervaleConfianceDomaine.objects.filter(domain_id__in=domain_ids) if domain_ids else IntervaleConfianceDomaine.objects.none()
    for intervalle in intervalles_d_query:
        data['intervalles_confiance_domaine'].append({
            'age': intervalle.age,
            'niveau_confiance': intervalle.niveau_confiance,
            'domain_name': domain_map.get(intervalle.domain_id, ''),
            'intervalle': intervalle.intervalle,
            'note_composite': intervalle.note_composite
        })
    
    # Export Niveaux Adaptatifs
    print("🎓 Export des niveaux adaptatifs...")
    for niveau in NiveauAdaptatif.objects.all():
        data['niveaux_adaptatifs'].append({
            'niveau': niveau.niveau,
            'echelle_v_min': niveau.echelle_v_min,
            'echelle_v_max': niveau.echelle_v_max,
            'note_standard_min': niveau.note_standard_min,
            'note_standard_max': niveau.note_standard_max
        })
    
    # Export Âges Équivalents
    print("👶 Export des âges équivalents...")
    ages_eq_query = AgeEquivalentSousDomaine.objects.filter(sous_domaine_id__in=sous_domain_ids) if sous_domain_ids else AgeEquivalentSousDomaine.objects.none()
    for age_eq in ages_eq_query:
        data['ages_equivalents'].append({
            'sous_domaine_name': sous_domain_map.get(age_eq.sous_domaine_id, ''),
            'note_brute_min': age_eq.note_brute_min,
            'note_brute_max': age_eq.note_brute_max,
            'age_special': age_eq.age_special,
            'age_annees': age_eq.age_annees,
            'age_mois': age_eq.age_mois
        })
    
    # Export Comparaisons Domaines
    print("⚖️ Export des comparaisons de domaines...")
    comp_d_query = ComparaisonDomaineVineland.objects.filter(domaine1_id__in=domain_ids, domaine2_id__in=domain_ids) if domain_ids else ComparaisonDomaineVineland.objects.none()
    for comp in comp_d_query:
        data['comparaisons_domaines'].append({
            'age': comp.age,
            'niveau_significativite': comp.niveau_significativite,
            'domaine1_name': domain_map.get(comp.domaine1_id, ''),
            'domaine2_name': domain_map.get(comp.domaine2_id, ''),
            'difference_requise': comp.difference_requise
        })
    
    # Export Comparaisons Sous-Domaines
    print("⚖️ Export des comparaisons de sous-domaines...")
    comp_sd_query = ComparaisonSousDomaineVineland.objects.filter(sous_domaine1_id__in=sous_domain_ids, sous_domaine2_id__in=sous_domain_ids) if sous_domain_ids else ComparaisonSousDomaineVineland.objects.none()
    for comp in comp_sd_query:
        data['comparaisons_sous_domaines'].append({
            'age': comp.age,
            'niveau_significativite': comp.niveau_significativite,
            'sous_domaine1_name': sous_domain_map.get(comp.sous_domaine1_id, ''),
            'sous_domaine2_name': sous_domain_map.get(comp.sous_domaine2_id, ''),
            'difference_requise': comp.difference_requise
        })
    
    # Export Fréquences Domaines
    print("📊 Export des fréquences de différence (domaines)...")
    freq_d_query = FrequenceDifferenceDomaineVineland.objects.filter(domaine1_id__in=domain_ids, domaine2_id__in=domain_ids) if domain_ids else FrequenceDifferenceDomaineVineland.objects.none()
    for freq in freq_d_query:
        data['frequences_domaines'].append({
            'age': freq.age,
            'domaine1_name': domain_map.get(freq.domaine1_id, ''),
            'domaine2_name': domain_map.get(freq.domaine2_id, ''),
            'frequence_16': freq.frequence_16,
            'frequence_10': freq.frequence_10,
            'frequence_5': freq.frequence_5
        })
    
    # Export Fréquences Sous-Domaines
    print("📊 Export des fréquences de différence (sous-domaines)...")
    freq_sd_query = FrequenceDifferenceSousDomaineVineland.objects.filter(sous_domaine1_id__in=sous_domain_ids, sous_domaine2_id__in=sous_domain_ids) if sous_domain_ids else FrequenceDifferenceSousDomaineVineland.objects.none()
    for freq in freq_sd_query:
        data['frequences_sous_domaines'].append({
            'age': freq.age,
            'sous_domaine1_name': sous_domain_map.get(freq.sous_domaine1_id, ''),
            'sous_domaine2_name': sous_domain_map.get(freq.sous_domaine2_id, ''),
            'frequence_16': freq.frequence_16,
            'frequence_10': freq.frequence_10,
            'frequence_5': freq.frequence_5
        })
    
    # Nom du fichier selon le formulaire
    if formulaire_filter:
        filename = f'{formulaire_filter.title.lower().replace(" ", "_")}_config_data.json'
    else:
        filename = 'all_tests_config_data.json'
    
    output_file = os.path.join(BASE_DIR, filename)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print("✅ EXPORT TERMINÉ")
    print("="*60)
    print(f"\n📁 Fichier créé : {output_file}\n")
    print("📊 Statistiques :")
    print(f"   - Formulaires: {len(data['formulaires'])}")
    print(f"   - Domaines: {len(data['domains'])}")
    print(f"   - Sous-Domaines: {len(data['sous_domains'])}")
    print(f"   - Questions: {len(data['questions'])}")
    print(f"   - Plages items: {len(data['plages_items'])}")
    print(f"   - Mappings Échelle-V: {len(data['echelle_v_mappings'])}")
    print(f"   - Mappings Notes Domaines: {len(data['note_domaine_mappings'])}")
    print(f"   - Intervalles Confiance (sous-domaines): {len(data['intervalles_confiance_sous_domaine'])}")
    print(f"   - Intervalles Confiance (domaines): {len(data['intervalles_confiance_domaine'])}")
    print(f"   - Niveaux Adaptatifs: {len(data['niveaux_adaptatifs'])}")
    print(f"   - Âges Équivalents: {len(data['ages_equivalents'])}")
    print(f"   - Comparaisons Domaines: {len(data['comparaisons_domaines'])}")
    print(f"   - Comparaisons Sous-Domaines: {len(data['comparaisons_sous_domaines'])}")
    print(f"   - Fréquences Domaines: {len(data['frequences_domaines'])}")
    print(f"   - Fréquences Sous-Domaines: {len(data['frequences_sous_domaines'])}")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    formulaire_choisi = choose_formulaire()
    export_data(formulaire_choisi)
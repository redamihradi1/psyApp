from django.core.management.base import BaseCommand
from vineland.models import QuestionVineland, PlageItemVineland
from polls.models import Domain, SousDomain

class Command(BaseCommand):
    help = 'Charge les questions Vineland pour Motricité Fine (5-6 ans)'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des questions Motricité Fine (5-6 ans)...')

        try:
            sous_domaine = SousDomain.objects.get(
                name='Fine',
                domain__name='Motricité'
            )

            plage, created = PlageItemVineland.objects.get_or_create(
                sous_domaine=sous_domaine,
                item_debut=11,
                item_fin=36,
                age_debut=5,
                age_fin=6
            )

            questions = [
                {
                    'numero_item': 11,
                    'texte': "Déballe de petits objets (par exemple, un chewing-gum ou un bonbon).",
                    'permet_na': False
                },
                {
                    'numero_item': 12,
                    'texte': "Fait des puzzles simples, comportant au moins deux formes ou deux pièces.",
                    'permet_na': False
                },
                {
                    'numero_item': 13,
                    'texte': "Tourne une à une les pages d\'un livre ou d\'un magazine.",
                    'permet_na': False
                },
                {
                    'numero_item': 14,
                    'texte': "Utilise un mouvement de rotation de la main ou du poignet (par exemple, remonte un jouet mécanique, visse/dévisse le couvercle d\'un pot, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 15,
                    'texte': "Tient correctement le crayon (pas à pleine main) pour dessiner ou écrire.",
                    'permet_na': False
                },
                {
                    'numero_item': 16,
                    'texte': "Colorie des formes simples ; peut dépasser.",
                    'permet_na': False
                },
                {
                    'numero_item': 17,
                    'texte': "Construit des structures en trois dimensions avec au moins 5 petits cubes (par exemple, une maison, un pont, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 18,
                    'texte': "Ouvre et ferme les ciseaux d\'une seule main.",
                    'permet_na': False
                },
                {
                    'numero_item': 19,
                    'texte': "Colle au moins 2 éléments ensemble (par exemple, pour un projet artistique ou scientifique).",
                    'permet_na': False
                },
                {
                    'numero_item': 20,
                    'texte': "Utilise du scotch pour faire tenir des choses ensemble (par exemple, une page déchirée, un projet artistique, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 21,
                    'texte': "Dessine plus d\'une forme reconnaissable (par exemple, un bonhomme, une maison, un arbre, etc.).",
                    'note': "Entourer 2 si il/elle dessine deux ou plusieurs formes reconnaissables|Entourer 1 si il/elle ne dessine qu\'une forme|Entourer 0 si il/elle ne dessine aucune forme reconnaissable",
                    'permet_na': True
                },
                {
                    'numero_item': 22,
                    'texte': "Écrit des lettres ou des chiffres reconnaissables.",
                    'permet_na': False
                },
                {
                    'numero_item': 23,
                    'texte': "Dessine un cercle à main levée en regardant un modèle.",
                    'permet_na': False
                },
                {
                    'numero_item': 24,
                    'texte': "Utilise des ciseaux pour couper un papier le long d\'une ligne droite.",
                    'permet_na': False
                },
                {
                    'numero_item': 25,
                    'texte': "Colorie des formes simples, sans dépasser.",
                    'permet_na': False
                },
                {
                    'numero_item': 26,
                    'texte': "Découpe des formes simples (par exemple, des cercles, des carrés, des rectangles, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 27,
                    'texte': "Utilise une gomme sans déchirer le papier.",
                    'permet_na': False
                },
                {
                    'numero_item': 28,
                    'texte': "Dessine un carré à main levée en regardant un modèle.",
                    'permet_na': False
                },
                {
                    'numero_item': 29,
                    'texte': "Dessine un triangle à main levée en regardant un modèle.",
                    'permet_na': False
                },
                {
                    'numero_item': 30,
                    'texte': "Fait un nœud.",
                    'permet_na': False
                },
                {
                    'numero_item': 31,
                    'texte': "Trace une ligne droite en utilisant une règle ou un bord droit.",
                    'permet_na': False
                },
                {
                    'numero_item': 32,
                    'texte': "Utilise un mouvement de rotation pour déverrouiller un verrou, ou tourner une clef dans une serrure.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a ni verrou, ni serrure au domicile",
                    'permet_na': True
                },
                {
                    'numero_item': 33,
                    'texte': "Découpe des formes complexes (par exemple, des étoiles, des animaux, les lettres de l\'alphabet, etc.).",
                    'permet_na': False
                },
                {
                    'numero_item': 34,
                    'texte': "Utilise un clavier, une machine à écrire ou un écran tactile pour taper un nom ou des mots courts ; peut regarder les touches.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a pas d\'ordinateur à la maison",
                    'permet_na': True
                },
                {
                    'numero_item': 35,
                    'texte': "Fait un double nœud.",
                    'permet_na': False
                },
                {
                    'numero_item': 36,
                    'texte': "Utilise un clavier pour taper jusqu\'à 10 lignes ; peut regarder les touches.",
                    'note': "Il est possible d\'entourer NA (Non Applicable) s\'il n\'y a pas d\'ordinateur à la maison",
                    'permet_na': True
                }
            ]

            for question_data in questions:
                question, created = QuestionVineland.objects.get_or_create(
                    sous_domaine=sous_domaine,
                    numero_item=question_data['numero_item'],
                    defaults={
                        'texte': question_data['texte'],
                        'permet_na': question_data['permet_na'],
                        'note': question_data.get('note', None)
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Question {question.numero_item} créée'))

            self.stdout.write(self.style.SUCCESS('Questions Motricité Fine (5-6 ans) chargées avec succès!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors du chargement : {str(e)}'))
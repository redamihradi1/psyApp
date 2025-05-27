from django.core.management.base import BaseCommand
from ...models import Formulaire, Domain, SousDomain, Question

class Command(BaseCommand):
    help = 'Import PEP3 questions and structure'

    def handle(self, *args, **kwargs):
        # Création du formulaire
        formulaire, created = Formulaire.objects.get_or_create(
            title='PEP3',
            description='Profil Psycho-Éducatif - 3ème édition'
        )
        self.stdout.write(self.style.SUCCESS(f'Formulaire créé: {formulaire.title}'))

        # Création des domaines principaux et leurs sous-domaines
        domains_data = {
            'Communication': ['CVP', 'LE', 'LR'],
            'Motricité': ['MF', 'MG', 'IOM'],
            'Comportements inadaptés': ['EA', 'RS', 'CMC', 'CVC']
        }

        domain_objects = {}
        for domain_name, sous_domains in domains_data.items():
            # Créer le domaine principal
            domain, created = Domain.objects.get_or_create(
                formulaire=formulaire,
                name=domain_name
            )
            domain_objects[domain_name] = domain
            
            # Créer les sous-domaines
            for sd_name in sous_domains:
                sous_domain, created = SousDomain.objects.get_or_create(
                    domain=domain,
                    name=sd_name
                )

        # Ajouter un domaine et sous-domaine "Autre" pour les instructions
        autre_domain, _ = Domain.objects.get_or_create(
            formulaire=formulaire,
            name='Autre'
        )
        autre_sous_domain, _ = SousDomain.objects.get_or_create(
            domain=autre_domain,
            name='Autre'
        )

        # Importer les questions
        questions_data  =[
                            {
                                "text": "Bulles",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Dévisse le couvercle d’un pot de bulles de savon",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Après démonstration, réussit à faire quelques bulles",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Suit clairement des yeux le déplacement des bulles de savon",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Suit bien le mouvement de bulles ou d'un autre objet traversant la ligne médiane",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Blocs tactiles",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Examine des cubes tactiles de façon appropriée",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Kaléidoscope",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Regarde dans un kaléidoscope et tourne le cylindre inférieur",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Présente une nette latéralisation oculaire",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Clochette",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "S'oriente vers le son d’une clochette",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Sonnette",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Imite et appuie deux fois sur une sonnette",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Pâte à modeler ou Playdooh (et 6 bâtonnets pour les items 11 et 12)",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Enfonce le doigt dans de la pâte à modeler en laissant un trou",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Prend un bâtonnet avec 2 ou 3 doigts pour l’enfoncer dans de la pâte à modeler ou le retirer ",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Après avoir écouté « Joyeux anniversaire », fait semblant d'éteindre les bougies",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Montre qu'il apprécie la musique en chantant ou en bougeant",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Après démonstration, fait un boudin avec de la pâte à modeler",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Marionnettes du chat ou du chien",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Met la main dans une marionnette et fait bouger sa tête et ses mains",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Imite des actions de tous les jours avec une marionnette",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Montre du doigt 3 parties du corps d’une marionnette",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Montre du doigt 3 parties de son propre corps",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Joue une histoire avec 2 marionnettes",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Fait preuve d'imagination lors du jeu avec les marionnettes",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Encastrement de formes - 3 pièces",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Indique pour 3 formes les bons emplacements dans un encastrement",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Insère 3 formes dans un  encastrement",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Nomme un rond, un carré et un triangle",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Sélectionne un rond, un carré, et un triangle lorsque l'examinateur les nomme",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Encastrement de 4 objets",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Place les formes dans un encastrement",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Traverse une ligne médiane pour prendre les pièces de l’'encastrement",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Encastrement des moufles",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Indique l’emplacement correct des 3 pièces",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Encastre correctement les 3 pièces",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Nomme des grandes et des petites formes",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Indique si une pièce  est grande ou petite",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Puzzle du chat",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Indique l’emplacement correct des pièces",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Assemble les 4 pièces du puzzle",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Puzzle de la vache",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Assemble les 6 pièces d’une image ",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Plaque aimantée ou puzzle du garçon",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Reconstitue un garçon composé de 8 pièces",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Claquette, clochette et cuillère",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Après démonstration, active 3 objets sonores",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Chaussette, verre, brosse à dents, crayon de couleur, ciseaux, peigne et feutre",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Nomme 5 objets",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Tasse, cuillère, crayon de couleur, peigne et ciseaux",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Montre comment se servir correctement de 4 objets",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Donne sur demande 3 objets à l'examinateur",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Livre d'images, chaussette, verre, brosse à dents, cuillère, ciseaux, peigne et crayon",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Fait correspondre 5 objets avec leur image",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Reconnaît les noms de 3 objets courants lorsqu’on les nomme",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "M&Ms",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Utilise le pouce et l’index pour saisir un bonbon M&M",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Tasse et petit objet apprécié",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Trouve un objet complètement dissimulé",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Aliment ou objet apprécié par l’enfant et 3 gobelets opaques",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Trouve un aliment ou un objet apprécié caché sous 1 des 3 gobelets et déplacé.",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Sac en toile contenant une cuillère, un cube, un feutre, une balle et un pion de jeu de dame",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Identifie au toucher 4 objets cachés dans un sac lorsque l’examinateur les nomme",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Examine et manipule le matériel du test de manière appropriée",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Regarde le matériel du test et l’environnement de façon appropriée",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Applaudit",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Se tient sur 1 pied",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Apprécie le contact physique de l’examinateur",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Apprécie les chatouillements de l’examinateur",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Serviette",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Initie la répétition d’un jeu social",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Initie des interactions sociales",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Saute à pieds joints",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Imite 3 mouvements de motricité globale",
                                "sous_domain": "IOM",
                                "can_ask": True
                            },
                            {
                                "text": "Escalier (de préférence sans rampe)",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Monte un escalier en alternant les pieds",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Gobelet et boisson appréciée par l’enfant",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Boit au gobelet sans renverser",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Sifflet",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Arrête une activité lorsqu’il entend un sifflet et cherche d’où vient le son",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Ballon en mousse de 20 à 25 cm de diamètre",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Attrape un ballon au moins 1 fois sur 3",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Lance un ballon au moins 1 fois sur 3",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Donne un coup de pied dans un ballon au moins 1 fois sur 3",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Se sert systématiquement du même pied pour taper dans le ballon, ou pour commencer à monter un escalier",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Fait au moins 4 pas en avant sans laisser tomber le ballon",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Pousse le ballon intentionnellement vers une cible",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Lacet avec un nœud à une extrémité",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Joue avec un lacet de façon appropriée",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "2 perles cubiques et un lacet avec un nœud à une extrémité",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Enfile une perle",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Balance les perles sur le lacet comme un pendule",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "6 perles cubiques et cure-pipe d’environ 25 cm",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Enlève 6 perles d’un cure-pipe en utilisant les mains de façon coordonnée",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise systématiquement ses mains de façon coordonnée",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Transfère des objets d’une main à l’autre",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Cahier d’écriture et feutre",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Gribouille spontanément",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Montre une latéralisation nette de la main : q Droite q Gauche",
                                "sous_domain": "MG",
                                "can_ask": True
                            },
                            {
                                "text": "Repasse sur 3 formes",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Copie une ligne verticale",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Copie un rond",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Copie un carré",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Copie un triangle",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Copie un losange",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Colorie à l’intérieur des lignes",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Recopie 7 lettres correctement",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Dessine un bonhomme (critères dans le Guide d'Administration des items)",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Ecrit son prénom",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Papier et ciseaux",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Coupe du papier avec des ciseaux",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Livre d'images",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "S’intéresse au Livre d’images",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Mime l’usage de 5 objets",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Désigne du doigt 14 images sur 20 quand l’examinateur les nomme (coter en utilisant la partie 8)",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Nomme correctement 14 images sur 20 (coter en utilisant la partie 8)",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Produit une phrase correcte de 4 ou 5 mots",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "9 lettres du loto (H,J,V,Z,U,E,Y,S,G)",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Identifie correctement 9 lettres",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Nomme 9 lettres correctement",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Livre d'images et 9 lettres du loto",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Place 9 lettres sur le loto",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Livre d'images",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Lit correctement des chiffres de 1 à 10",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Lit 3 mots",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Lit correctement 1 phrase courte (coter en utilisant la partie 8)",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Lit un passage en ne faisant pas plus de 3 erreurs (coter en utilisant la partie 8)",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Lit un passage et répond correctement à 2 questions de compréhension (coter en utilisant la partie 8)",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Livre d'images, balle de 3-4 cm de diamètre, boîte de tri",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Lit une phrase et suit les consignes",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "6 cubes et boîte de tri",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Met un cube dans une boîte",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Met des cubes dans une boîte à tour de rôle",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "12 cubes",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Empile 8 cubes",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Tasse et cubes",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Exécute une consigne en 2 parties",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "8 cubes de même couleur",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Donne 2 cubes et 6 cubes à la demande de l’examinateur",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "7 cubes de même couleur",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Compte 2 et 7 cubes",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Compte de 1 à 10 à voix haute",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "6 cubes de même couleur, 6 pions noirs et 2 boîtes de tri",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Trie 6 cubes et 6 pions dans des boîtes séparées",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Livre d’images et 5 cubes de couleur (jaune, rouge, bleu, vert, blanc)",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Associe 5 cubes de couleur à 5 ronds de couleur",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Nomme 5 couleurs",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Désigne 5 couleurs quand l’examinateur les nomme",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "12 cartes de catégorie (losanges, cercles, carrés, triangles, en vert, rouge et violet)",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Trie 12 cartes par couleur ou par forme sans démonstration",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Réagit à l’imitation de ses propres actions",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Réagit à l’imitation de ses propres sons",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Répète 3 sons émis par l’examinateur",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Répète 2 chiffres",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Répète 3 chiffres",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Répète 2 mots",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Répète 2 phrases de 3 à 4 mots",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Réagit au langage en regardant directement le visage de l’examinateur",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Ne répète pas de façon inappropriée des mots ou des phrases après un certain délai",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Aliments, petite assiette, gobelet de jus de fruit",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Demande à manger ou à boire.",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Montre une certaine compréhension des pronoms personnels",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Biscuits, cubes, gobelets\t",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Utilise 2 substantifs au pluriel",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Jus de fruit, 2 gobelets, biscuits, marionnette d’animal",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Utilise 1 pronom",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Jus de fruit, gobelet, biscuit, peigne, bulles",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Emet 3 phrases appropriées de 2 mots",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Balle de 3-4 cm, gobelet, marionnette du chien et boîte assez grande pour contenir un sac en toile",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Exécute 4 consignes à 1 ou 2 étapes",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Interrupteur (dans le local d’évaluation)",
                                "sous_domain": "Autre",
                                "can_ask": False
                            },
                            {
                                "text": "Actionne un interrupteur",
                                "sous_domain": "MF",
                                "can_ask": True
                            },
                            {
                                "text": "Réagit systématiquement aux gestes",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Arrête ce qu’il est en train de faire en réponse à \"Non !`\"  ou \"Arrête !\"",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Arrête ce qu’il est en train de faire quand on dit son prénom",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Comprend la consigne simple « Viens ici »",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Dit son nom quand on le lui demande",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Précise son sexe lorsqu'on le lui demande",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Montre qu'il comprend le sens de 3 verbes d'action",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise des pronoms correctement",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Répond aux questions commençant par qui, que,  où et quand ",
                                "sous_domain": "LR",
                                "can_ask": True
                            },
                            {
                                "text": "Suit 3 consignes composées d'une seule action",
                                "sous_domain": "CVP",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise des informations visuelles de façon appropriée",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Joue seul en utilisant l'espace et le matériel de façon appropriée à l'âge",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Explore de façon appropriée l'environnement de l’évaluation ",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Ecoute de façon appropriée l'examinateur et les sons émis ",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Examine les textures de façon appropriée",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Goûte à la nourriture pendant l’évaluation et ne porte pas à la bouche ou ne lèche pas les objets de façon inappropriée",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Montre un intérêt olfactif approprié",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Réalise la plupart des activités adaptées à son âge",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise des mots ou des gestes pour obtenir de l'aide",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Ne répète pas de façon inappropriée des mots ou des phrases entendus récemment",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Ne répète pas continuellement certains mots ou certains sons",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Parle avec une intonation, un débit et un volume normaux ",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Emet rarement des sons sans signification ou inintelligibles",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise principalement des mots appropriés à son âge pour communiquer avec les autres",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "N'utilise pas un langage idiosyncrasique ou un jargon",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Articule correctement pour son âge",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Montre une communication spontanée appropriée à son âge",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Communique spontanément avec l'examinateur",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Poursuit une conversation plus longtemps qu’un simple échange",
                                "sous_domain": "CVC",
                                "can_ask": True
                            },
                            {
                                "text": "Essaie de collaborer aux demandes de l’évaluateur",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise une syntaxe appropriée à son âge",
                                "sous_domain": "LE",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise des expressions faciales pour exprimer ses sentiments",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Exprime ses sentiments  ou sensations par les positions de son corps",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Exprime des émotions appropriées au cours de l’évaluation",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Manifeste des marques d'affection appropriées au cours de l’évaluation",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Manifeste un niveau de peur approprié au cours de l’évaluation",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Manifeste un temps d’attention approprié à son âge",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Passe facilement d’une activité à une autre",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise le raisonnement par essais-erreurs pour se corriger",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Réalise avec persévérance des activités appropriées à son développement ",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Attire l’attention de l’examinateur sur ses intérêts et compétences particuliers",
                                "sous_domain": "EA",
                                "can_ask": True
                            },
                            {
                                "text": "Maintient le contact visuel tout au long de l’évaluation",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Montre qu'il reconnaît la voix de l’examinateur par ses actions",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Recherche l’aide de l’examinateur de manière appropriée",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "Utilise son corps de manière appropriée à son âge",
                                "sous_domain": "CMC",
                                "can_ask": True
                            },
                            {
                                "text": "Réagit à l’examinateur de manière appropriée, établit le contact visuel, écoute et sourit",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "La performance de l'enfant est influencée par les récompenses concrètes",
                                "sous_domain": "RS",
                                "can_ask": True
                            },
                            {
                                "text": "La performance de l'enfant est influencée par les félicitations sociales",
                                "sous_domain": "RS",
                                "can_ask": True
                            }
                            ]


        for q_data in questions_data:
            sous_domain = SousDomain.objects.get(name=q_data['sous_domain'])
            Question.objects.get_or_create(
                sous_domain=sous_domain,
                text=q_data['text'],
                can_ask=q_data['can_ask']
            )

        self.stdout.write(self.style.SUCCESS('Import terminé'))
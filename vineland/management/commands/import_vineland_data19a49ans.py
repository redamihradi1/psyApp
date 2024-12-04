from django.core.management.base import BaseCommand
from vineland.models import NoteDomaineVMapping

class Command(BaseCommand):
    help = 'Import des données de correspondance pour la tranche 19-49 ans'

    def handle(self, *args, **options):
        mappings_19_49_ans = [
            # Format: (note_standard, comm, vie_quot, social, note_comp_min, note_comp_max, rang)
            (160, None, None, None, None, None, '>99'),
            (159, None, None, None, None, None, '>99'),
            (158, None, None, None, None, None, '>99'),
            (157, None, None, None, None, None, '>99'),
            (156, None, None, None, None, None, '>99'),
            (155, None, None, None, None, None, '>99'),
            (154, None, None, None, None, None, '>99'),
            (153, None, None, None, None, None, '>99'),
            (152, None, None, None, None, None, '>99'),
            (151, None, None, None, None, None, '>99'),
            (150, None, None, None, None, None, '>99'),
            (149, None, None, None, None, None, '>99'),
            (148, None, None, None, None, None, '>99'),
            (147, None, None, None, None, None, '>99'),
            (146, None, None, None, None, None, '>99'),
            (145, None, None, None, None, None, '>99'),
            (144, None, None, None, None, None, '>99'),
            (143, None, None, None, None, None, '>99'),
            (142, None, None, None, None, None, '>99'),
            (141, None, None, None, None, None, '>99'),
            (140, None, None, None, None, None, '>99'),
            (139, None, None, None, None, None, '>99'),
            (138, None, None, None, None, None, 99),
            (137, None, None, None, None, None, 99),
            (136, None, None, None, None, None, 99),
            (135, None, None, None, None, None, 99),
            (134, None, None, None, None, None, 99),
            (133, None, None, None, None, None, 99),
            (132, None, None, None, None, None, 98),
            (131, None, None, None, None, None, 98),
            (130, None, None, None, None, None, 98),
            (129, None, None, None, None, None, 97),
            (128, None, None, None, None, None, 97),
            (127, None, 56, None, None, None, 96),
            (126, None, None, None, None, None, 96),
            (125, None, None, None, None, None, 95),
            (124, None, 55, None, None, None, 95),
            (123, None, None, None, None, None, 94),
            (122, None, None, None, 355, 355, 93),
            (121, None, 54, None, 352, 354, 92),
            (120, None, None, None, 350, 351, 91),
            (119, None, 53, None, 347, 349, 90),
            (118, None, None, 49, 345, 346, 88),
            (117, None, None, None, 342, 344, 87),
            (116, None, 52, None, 340, 341, 86),
            (115, None, None, None, 338, 339, 84),
            (114, None, 51, 48, 335, 337, 82),
            (113, None, None, None, 333, 334, 81),
            (112, None, 50, 47, 330, 332, 79),
            (111, None, None, None, 328, 329, 77),
            (110, 48, None, None, 325, 327, 75),
            (109, None, 49, 46, 323, 324, 73),
            (108, None, None, None, 321, 322, 70),
            (107, 47, 48, None, 318, 320, 68),
            (106, None, None, None, 316, 317, 66),
            (105, None, None, 45, 313, 315, 63),
            (104, 46, 47, None, 311, 312, 61),
            (103, None, None, None, 308, 310, 58),
            (102, None, 46, 44, 306, 307, 55),
            (101, 45, None, None, 304, 305, 53),
            (100, None, 45, None, 301, 303, 50),
            (99, 44, None, 43, 299, 300, 47),
            (98, None, None, None, 296, 298, 45),
            (97, 43, 44, None, 294, 295, 42),
            (96, None, None, 42, 291, 293, 39),
            (95, None, None, None, 289, 290, 37),
            (94, 42, 43, None, 286, 288, 34),
            (93, None, None, None, 284, 285, 32),
            (92, None, None, None, 282, 283, 30),
            (91, 41, 42, None, 279, 281, 27),
            (90, 41, None, None, 277, 278, 25),
            (89, None, 41, 40, 274, 276, 23),
            (88, None, None, None, 272, 273, 21),
            (87, 40, None, None, 269, 271, 19),
            (86, None, 40, 39, 267, 268, 18),
            (85, 39, None, None, 265, 266, 16),
            (84, None, 39, None, 262, 264, 14),
            (83, None, None, None, 260, 261, 13),
            (82, 38, None, 38, 257, 259, 12),
            (81, None, 38, None, 255, 256, 10),
            (80, None, None, None, 252, 254, 9),
            (79, 37, None, 37, 250, 251, 8),
            (78, None, 37, None, 248, 249, 7),
            (77, None, None, 36, 245, 247, 6),
            (76, 36, 36, None, 243, 244, 5),
            (75, None, None, None, 240, 242, 5),
            (74, None, None, None, 238, 239, 4),
            (73, 35, None, 35, 235, 237, 4),
            (72, None, None, None, 233, 234, 3),
            (71, 34, None, None, 230, 232, 3),
            (70, None, 34, None, 228, 229, 2),
            (69, 33, None, 34, 226, 227, 2),
            (68, None, 33, None, 223, 225, 2),
            (67, None, None, None, 221, 222, 1),
            (66, 32, None, 33, 218, 220, 1),
            (65, None, 32, None, 216, 217, 1),
            (64, None, None, None, 213, 215, 1),
            (63, 31, 31, 32, 211, 212, 1),
            (62, None, None, None, 209, 210, 1),
            (61, 30, 30, 31, 206, 208, '<1'),
            (60, None, None, None, 204, 205, '<1'),
            (59, 29, 29, None, 201, 203, '<1'),
            (58, None, None, 30, 199, 200, '<1'),
            (57, 28, 28, None, 196, 198, '<1'),
            (56, None, None, 29, 192, 195, '<1'),
            (55, 27, 27, None, 189, 191, '<1'),
            (54, None, None, None, 187, 188, '<1'),
            (53, 26, 26, 28, 184, 186, '<1'),
            (52, None, None, None, 182, 183, '<1'),
            (51, 25, 25, 27, 179, 181, '<1'),
            (50, None, None, None, 177, 178, '<1'),
            (49, 24, 24, None, 175, 176, '<1'),
            (48, None, None, None, 172, 174, '<1'),
            (47, 23, 23, 26, 170, 171, '<1'),
            (46, None, None, None, 167, 169, '<1'),
            (45, 22, 22, 25, 165, 166, '<1'),
            (44, None, None, None, 162, 164, '<1'),
            (43, 21, 21, 24, 160, 161, '<1'),
            (42, None, None, None, 157, 159, '<1'),
            (41, 20, 20, 23, 155, 156, '<1'),
            (40, None, None, None, 150, 154, '<1'),
            (39, 19, 19, 22, 148, 149, '<1'),
            (38, None, None, None, 146, 147, '<1'),
            (37, 18, 18, 21, 143, 145, '<1'),
            (36, None, None, None, 140, 142, '<1'),
            (35, 17, 17, None, 138, 139, '<1'),
            (34, None, None, None, 135, 137, '<1'),
            (33, 16, 16, None, 133, 134, '<1'),
            (32, None, None, None, 131, 132, '<1'),
            (31, None, None, None, 128, 130, '<1'),
            (30, None, None, None, 126, 127, '<1'),
            (29, None, None, None, 123, 125, '<1'),
            (28, None, None, None, 121, 122, '<1'),
            (27, None, None, None, 118, 120, '<1'),
            (26, None, None, None, 116, 117, '<1'),
            (25, None, None, None, 114, 115, '<1'),
            (24, None, None, None, 111, 113, '<1'),
            (23, None, None, None, 109, 110, '<1'),
            (22, None, None, None, None, None, '<1'),
            (21, None, None, None, None, None, '<1'),
            (20, "3-16", "3-15", "3-19", 60, 108, '<1')
        ]

        # Suppression des anciennes données pour la tranche 19-49 ans
        NoteDomaineVMapping.objects.filter(tranche_age='19-49').delete()

        # Import des nouvelles données
        for mapping in mappings_19_49_ans:
            note_std, comm, vie_quot, social, note_comp_min, note_comp_max, rang = mapping
            
            # Traitement pour la communication
            comm_min = None
            comm_max = None
            if isinstance(comm, str) and '-' in comm:
                comm_min, comm_max = map(int, comm.split('-'))
            elif comm is not None:
                comm_min = comm_max = comm
                
            # Traitement pour la vie quotidienne
            vie_quot_min = None
            vie_quot_max = None
            if isinstance(vie_quot, str) and '-' in vie_quot:
                vie_quot_min, vie_quot_max = map(int, vie_quot.split('-'))
            elif vie_quot is not None:
                vie_quot_min = vie_quot_max = vie_quot
                
            # Traitement pour la socialisation
            social_min = None
            social_max = None
            if isinstance(social, str) and '-' in social:
                social_min, social_max = map(int, social.split('-'))
            elif social is not None:
                social_min = social_max = social

            try:
                NoteDomaineVMapping.objects.create(
                    tranche_age='19-49',
                    note_standard=note_std,
                    communication_min=comm_min,
                    communication_max=comm_max,
                    vie_quotidienne_min=vie_quot_min,
                    vie_quotidienne_max=vie_quot_max,
                    socialisation_min=social_min,
                    socialisation_max=social_max,
                    motricite_min=None,  # Pas de motricité pour cette tranche d'âge
                    motricite_max=None,
                    note_composite_min=note_comp_min,
                    note_composite_max=note_comp_max,
                    rang_percentile=rang
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Erreur lors de l\'import de la note standard {note_std}: {str(e)}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                'Import réussi des données pour la tranche 19-49 ans'
            )
        )
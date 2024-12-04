from django.core.management.base import BaseCommand
from vineland.models import NoteDomaineVMapping

class Command(BaseCommand):
    help = 'Import des données de correspondance pour la tranche 7-18 ans'

    def handle(self, *args, **options):
        mappings_7_18_ans = [
            # Format: (note_standard, comm, vie_quot, social, motric, note_comp_min, note_comp_max, rang)
            (160, None, "70-72", None, None, 447, 480, '>99'),
            (159, None, 69, None, None, 445, 446, '>99'),
            (158, None, None, None, None, 442, 444, '>99'),
            (157, None, 68, None, None, 440, 441, '>99'),
            (156, None, None, None, None, 437, 439, '>99'),
            (155, None, 67, 71, None, 435, 436, '>99'),
            (154, None, None, None, None, 432, 434, '>99'),
            (153, None, 66, 70, None, 430, 431, '>99'),
            (152, None, None, None, None, 427, 429, '>99'),
            (151, None, 65, 69, None, 425, 426, '>99'),
            (150, None, None, 68, None, 422, 424, '>99'),
            (149, None, None, None, None, 420, 421, '>99'),
            (148, None, 64, 67, None, 417, 419, '>99'),
            (147, None, None, None, None, 415, 416, '>99'),
            (146, None, None, 66, None, 412, 414, '>99'),
            (145, 63, 63, None, None, 410, 411, '>99'),
            (144, None, None, None, None, 407, 409, '>99'),
            (143, None, 62, 65, None, 405, 406, '>99'),
            (142, 62, None, None, None, 402, 404, '>99'),
            (141, None, None, 64, None, 400, 401, '>99'),
            (140, 61, 61, None, None, 397, 399, '>99'),
            (139, None, None, 63, None, 395, 396, '>99'),
            (138, None, 60, None, None, 392, 394, 99),
            (137, 60, None, 62, None, 390, 391, 99),
            (136, None, 59, None, None, 387, 389, 99),
            (135, 59, None, 61, None, 385, 386, 99),
            (134, None, 58, None, None, 382, 384, 99),
            (133, 58, None, 60, None, 380, 381, 99),
            (132, None, 57, None, None, 377, 379, 98),
            (131, 57, None, 59, None, 375, 376, 98),
            (130, None, None, None, None, 372, 374, 98),
            (129, None, 56, 58, None, 370, 371, 97),
            (128, None, None, None, None, 367, 369, 97),
            (127, 56, 55, 57, None, 365, 366, 96),
            (126, None, None, None, None, 362, 364, 96),
            (125, None, 54, 56, None, 360, 361, 95),
            (124, 55, None, None, None, 358, 359, 95),
            (123, None, None, 55, None, 355, 357, 94),
            (122, 54, 53, None, None, 353, 354, 93),
            (121, None, None, 54, None, 350, 352, 92),
            (120, None, 52, None, None, 348, 349, 91),
            (119, 53, None, 53, None, 345, 347, 90),
            (118, None, 51, None, None, 343, 344, 88),
            (117, 52, None, None, None, 340, 342, 87),
            (116, None, None, 52, None, 338, 339, 86),
            (115, 51, 50, None, None, 335, 337, 84),
            (114, None, None, 51, None, 333, 334, 82),
            (113, 50, 49, None, None, 330, 332, 81),
            (112, None, None, 50, None, 328, 329, 79),
            (111, None, 48, None, None, 325, 327, 77),
            (110, 49, None, 49, None, 323, 324, 75),
            (109, None, None, None, None, 320, 322, 73),
            (108, None, 47, 48, None, 318, 319, 70),
            (107, None, None, None, None, 315, 317, 68),
            (106, 48, 46, 47, None, 313, 314, 66),
            (105, None, None, None, None, 310, 312, 63),
            (104, 47, None, None, None, 308, 309, 61),
            (103, None, 45, None, None, 305, 307, 58),
            (102, None, None, 46, None, 303, 304, 55),
            (101, 46, None, None, None, 300, 302, 53),
            (100, None, 44, 45, None, 298, 299, 50),
            (99, 45, None, None, None, 295, 297, 47),
            (98, None, 43, 44, None, 293, 294, 45),
            (97, None, None, None, None, 290, 292, 42),
            (96, 44, 42, 43, None, 288, 289, 39),
            (95, None, None, None, None, 285, 287, 37),
            (94, 43, None, 42, None, 283, 284, 34),
            (93, None, 41, None, None, 280, 282, 32),
            (92, None, None, 41, None, 278, 279, 30),
            (91, 42, 40, None, None, 275, 277, 27),
            (90, 41, None, 40, None, 273, 274, 25),
            (89, None, 39, None, None, 270, 272, 23),
            (88, None, None, 39, None, 268, 269, 21),
            (87, 40, 38, None, None, 265, 267, 19),
            (86, None, None, 38, None, 263, 264, 18),
            (85, None, 37, 37, None, 260, 262, 16),
            (84, 39, None, None, None, 258, 259, 14),
            (83, None, 36, 36, None, 255, 257, 13),
            (82, 38, 35, None, None, 253, 254, 12),
            (81, None, None, 35, None, 251, 252, 10),
            (80, None, 34, 34, None, 248, 250, 9),
            (79, 37, None, None, None, 246, 247, 8),
            (78, None, 33, 33, None, 243, 245, 7),
            (77, 36, None, None, None, 241, 242, 6),
            (76, None, 32, 32, None, 238, 240, 5),
            (75, 35, None, None, None, 236, 237, 5),
            (74, None, 31, 31, None, 233, 235, 4),
            (73, None, None, None, None, 231, 232, 3),
            (72, 34, 30, 30, None, 228, 230, 3),
            (71, None, None, None, None, 226, 227, 3),
            (70, 33, 29, 29, None, 223, 225, 2),
            (69, None, None, None, None, 221, 222, 2),
            (68, 32, 28, 28, None, 218, 220, 2),
            (67, None, None, None, None, 216, 217, 1),
            (66, 31, 27, 27, None, 213, 215, 1),
            (65, None, None, None, None, 211, 212, 1),
            (64, 30, 26, 26, None, 208, 210, 1),
            (63, None, None, None, None, 206, 207, 1),
            (62, 29, 25, 25, None, 203, 205, 1),
            (61, None, None, None, None, 201, 202, '<1'),
            (60, 28, 24, 24, None, 198, 200, '<1'),
            (59, None, None, None, None, 196, 197, '<1'),
            (58, 27, 23, 23, None, 193, 195, '<1'),
            (57, None, None, None, None, 191, 192, '<1'),
            (56, 26, 22, 22, None, 188, 190, '<1'),
            (55, None, None, None, None, 186, 187, '<1'),
            (54, 25, 21, 21, None, 183, 185, '<1'),
            (53, None, None, None, None, 181, 182, '<1'),
            (52, 24, 20, 20, None, 178, 180, '<1'),
            (51, None, None, None, None, 176, 177, '<1'),
            (50, 23, 19, 19, None, 173, 175, '<1'),
            (49, None, None, None, None, 171, 172, '<1'),
            (48, 22, 18, 18, None, 168, 170, '<1'),
            (47, None, None, None, None, 166, 167, '<1'),
            (46, 21, 17, 17, None, 163, 165, '<1'),
            (45, None, None, None, None, 161, 162, '<1'),
            (44, 20, 16, 16, None, 158, 160, '<1'),
            (43, None, None, None, None, 156, 157, '<1'),
            (42, 19, 15, 15, None, 153, 155, '<1'),
            (41, None, None, None, None, 151, 152, '<1'),
            (40, 18, None, 14, None, 148, 150, '<1'),
            (39, None, None, None, None, 146, 147, '<1'),
            (38, 17, 13, 13, None, 144, 145, '<1'),
            (37, None, None, None, None, 141, 143, '<1'),
            (36, 16, 12, 12, None, 139, 140, '<1'),
            (35, None, None, None, None, 136, 138, '<1'),
            (34, 15, 11, 11, None, 134, 135, '<1'),
            (33, None, None, None, None, 131, 133, '<1'),
            (32, None, None, None, None, 129, 130, '<1'),
            (31, None, None, None, None, 126, 128, '<1'),
            (30, None, None, None, None, 124, 125, '<1'),
            (29, None, None, None, None, 121, 123, '<1'),
            (28, None, None, None, None, 119, 120, '<1'),
            (27, None, None, None, None, 116, 118, '<1'),
            (26, None, None, None, None, 114, 115, '<1'),
            (25, None, None, None, None, 111, 113, '<1'),
            (24, None, None, None, None, 109, 110, '<1'),
            (23, None, None, None, None, 106, 108, '<1'),
            (22, None, None, None, None, 104, 105, '<1'),
            (21, None, None, None, None, 101, 103, '<1'),
            (20, "3-14", "3-10", "3-8", None, 60, 100, '<1')
        ]

        # Suppression des anciennes données pour la tranche 7-18 ans
        NoteDomaineVMapping.objects.filter(tranche_age='7-18').delete()

        # Import des nouvelles données
        for mapping in mappings_7_18_ans:
            note_std, comm, vie_quot, social, motric, comp_min, comp_max, rang = mapping
            
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
                
            # Traitement pour la motricité
            motric_min = None
            motric_max = None
            if isinstance(motric, str) and '-' in motric:
                motric_min, motric_max = map(int, motric.split('-'))
            elif motric is not None:
                motric_min = motric_max = motric

            try:
                NoteDomaineVMapping.objects.create(
                    tranche_age='7-18',
                    note_standard=note_std,
                    communication_min=comm_min,
                    communication_max=comm_max,
                    vie_quotidienne_min=vie_quot_min,
                    vie_quotidienne_max=vie_quot_max,
                    socialisation_min=social_min,
                    socialisation_max=social_max,
                    motricite_min=motric_min,
                    motricite_max=motric_max,
                    note_composite_min=comp_min,
                    note_composite_max=comp_max,
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
                'Import réussi des données pour la tranche 1-2 ans'
            )
        )
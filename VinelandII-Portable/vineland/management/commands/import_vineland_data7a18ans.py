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
			
            (155, None, None, 71, None, 435, 436, '>99'),
            (154, None, None, None, None, 432, 434, '>99'),
            (153, None, None, 70, None, 430, 431, '>99'),
            (152, None, 66, None, None, 427, 429, '>99'),
            (151, None, None, 69, None, 425, 426, '>99'),
			
            (150, None, 65, None, None, 422, 424, '>99'),
            (149, None, None, 68, None, 420, 421, '>99'),
            (148, None, None, None, None, 417, 419, '>99'),
            (147, None, 64, 67, None, 415, 416, '>99'),
            (146, None, None, None, None, 412, 414, '>99'),
			
            (145, 63, 63, None, None, 410, 411, '>99'),
            (144, None, None, 66, None, 407, 409, '>99'),
            (143, None, 62, None, None, 405, 406, '>99'),
            (142, 62, None, None, 65, 402, 404, '>99'),
            (141, None, None, None, None, 400, 401, '>99'),
			
            (140, 61, 61, 64, None, 397, 399, '>99'),
            (139, None, None, None, None, 395, 396, '>99'),
            (138, None, 60, None, None, 392, 394, 99),
            (137, 60, None, None, None, 390, 391, 99),
            (136, None, 59, 62 , None, 387, 389, 99),
			
            (135, 59, None, None, None, 385, 386, 99),
            (134, None, None, 61, None, 382, 384, 99),
            (133, None, 58, None, None, 380, 381, 99),
            (132, 58, None, 60, None, 377, 379, 98),
            (131, None, 57, None, None, 375, 376, 98),
			
            (130, 57, None, None, None, 372, 374, 98),
            (129, None, None, 59, None, 370, 371, 97),
            (128, None, None, None, None, 367, 369, 97),
            (127, 56, 55, 57, None, 365, 366, 96),
            (126, None, None, None, None, 362, 364, 96),
			
            (125, None, None, 57, None, 360, 361, 95),
            (124, 55, 54, None, None, 358, 359, 95),
            (123, None, None, 56, None, 355, 357, 94),
            (122, 54, None, None, None, 353, 354, 93),
            (121, None, 53, None, None, 350, 352, 92),
			
            (120, None, None, None, None, 348, 349, 91),
            (119, 53, 52, None, None, 345, 347, 90),
            (118, None, None, None, None, 343, 344, 88),
            (117, 52, 51, None, None, 340, 342, 87),
            (116, None, None, 53, None, 338, 339, 86),
			
            (115, None, None, None, None, 335, 337, 84),
            (114, 51, 50, 52, None, 333, 334, 82),
            (113, None, None, None, None, 330, 332, 81),
            (112, 50, 49, 51, None, 328, 329, 79),
            (111, None, None, None, None, 325, 327, 77),
			
            (110, None, 48, 50, None, 323, 324, 75),
            (109, 49, None, None, None, 320, 322, 73),
            (108, None, None, 49, None, 318, 319, 70),
            (107, None, 47, None, None, 315, 317, 68),
            (106, 48, None, 47, None, 313, 314, 66),
			
            (105, None, 46, None, None, 310, 312, 63),
            (104, 47, None, 47, None, 308, 309, 61),
            (103, None, None, None, None, 305, 307, 58),
            (102, None, 45, None, None, 303, 304, 55),
            (101, 46, None, 46, None, 300, 302, 53),
			
            (100, None, 44, None, None, 298, 299, 50),
            (99, 45, None, 45, None, 295, 297, 47),
            (98, None, 43, None, None, 293, 294, 45),
            (97, None, None, 44, None, 290, 292, 42),
            (96, 44, None, None, None, 288, 289, 39),
			
            (95, None, 42, 43, None, 285, 287, 37),
            (94, 43, None, None, None, 283, 284, 34),
            (93, None, 41, 42, None, 280, 282, 32),
            (92, None, None, None, None, 278, 279, 30),
            (91, 42, 40, 41, None, 275, 277, 27),
			
            (90, 41, None, 40, None, 273, 274, 25),
            (89, None, 39, None, None, 270, 272, 23),
            (88, None, None, 39, None, 268, 269, 21),
            (87, 40, 38, None, None, 265, 267, 19),
            (86, None, None, 38, None, 263, 264, 18),
			
            (85, None, None, None, None, 260, 262, 16),
            (84, None, 37, 38, None, 258, 259, 14),
            (83, 37, None, None, None, 255, 257, 13),
            (82, None, None, 37, None, 253, 254, 12),
            (81, 38, 36, None, None, 251, 252, 10),
			
            (80, None, None, 36, None, 248, 250, 9),
            (79, None, 35, None, None, 246, 247, 8),
            (78, 37, None, 35, None, 243, 245, 7),
            (77, None, None, None, None, 241, 242, 6),
            (76, 34, 34, 34, None, 238, 240, 5),
			
            (75, None, None, None, None, 236, 237, 5),
            (74, None, 33, None, None, 233, 235, 4),
            (73, None, None, None, None, 231, 232, 3),
            (72, None, 32, None, None, 228, 230, 3),
            (71, 34, None, 32, None, 226, 227, 3),
			
            (70, None, None, None, None, 223, 225, 2),
            (69, None, 31, 31, None, 221, 222, 2),
            (68, 33, None, None, None, 218, 220, 2),
            (67, None, 30, 30, None, 216, 217, 1),
            (66, 32, None, None, None, 213, 215, 1),
			
            (65, None, 29, 29, None, 211, 212, 1),
            (64, None, None, None, None, 208, 210, 1),
            (63, 31, None, 28, None, 206, 207, 1),
            (62, None, 28, None, None, 203, 205, 1),
            (61, None, None, 27, None, 201, 202, '<1'),
			
            (60, 30, 27, None, None, 198, 200, '<1'),
            (59, None, None, None, None, 196, 197, '<1'),
            (58, 29, 26, 26, None, 193, 195, '<1'),
            (57, None, None, None, None, 191, 192, '<1'),
            (56, None, None, 25, None, 188, 190, '<1'),
			
            (55, 28, 25, None, None, 186, 187, '<1'),
            (54, None, None, 24, None, 183, 185, '<1'),
            (53, 27, 24, None, None, 181, 182, '<1'),
            (52, None, None, 23, None, 178, 180, '<1'),
            (51, None, None, None, None, 176, 177, '<1'),
			
            (50, 26, 23, 22, None, 173, 175, '<1'),
            (49, None, None, None, None, 171, 172, '<1'),
            (48, 25, 22, 21, None, 168, 170, '<1'),
            (47, None, None, None, None, 166, 167, '<1'),
            (46, None, 21, None, None, 163, 165, '<1'),
			
            (45, 24, None, 20, None, 161, 162, '<1'),
            (44, None, None, None, None, 158, 160, '<1'),
            (43, None, 20, 19, None, 156, 157, '<1'),
            (42, 23, None, None, None, 153, 155, '<1'),
            (41, None, 19, 18, None, 151, 152, '<1'),
			
            (40, 22, None, None, None, 148, 150, '<1'),
            (39, None, 18, 17, None, 146, 147, '<1'),
            (38, 17, 13, 13, None, 144, 145, '<1'),
            (37, 21, None, 16, None, 141, 143, '<1'),
            (36, None, 17, None, None, 139, 140, '<1'),
			
            (35, 20, None, 15, None, 136, 138, '<1'),
            (34, 15, 16, None, None, 134, 135, '<1'),
            (33, None, None, 14, None, 131, 133, '<1'),
            (32, 19, None, None, None, 129, 130, '<1'),
            (31, None, 15, None, None, 126, 128, '<1'),
			
            (30, 18, None, 13, None, 124, 125, '<1'),
            (29, None, 14, None, None, 121, 123, '<1'),
            (28, None, None, None, None, 119, 120, '<1'),
            (27, 17, 13, None, None, 116, 118, '<1'),
            (26, None, None, 11, None, 114, 115, '<1'),
			
            (25, 16, None, None, None, 111, 113, '<1'),
            (24, None, 12, 10, None, 109, 110, '<1'),
            (23, None, None, None, None, 106, 108, '<1'),
            (22, 15, 11, None, 9, 104, 105, '<1'),
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
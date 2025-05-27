from django.core.management.base import BaseCommand
from vineland.models import NoteDomaineVMapping

class Command(BaseCommand):
    help = 'Import des données de correspondance pour la tranche 3-6 ans'

    def handle(self, *args, **options):
        mappings_3_6_ans = [
            # Format: (note_standard, comm, vie_quot, social, motric, note_comp_min, note_comp_max, rang)
            (160, 72, "71-72", None, None, 591, 640, '>99'),
            (159, None, 70, 72, None, 588, 590, '>99'),
            (158, 71, None, None, None, 585, 587, '>99'),
            (157, None, None, 71, None, 581, 584, '>99'),
            (156, 70, 69, None, None, 578, 580, '>99'),
			
            (155, None, None, 70, None, 575, 577, '>99'),
            (154, 69, 68, None, None, 572, 574, '>99'),
            (153, None, None, None, None, 569, 571, '>99'),
            (152, None, 67, 69, None, 565, 568, '>99'),
            (151, 68, None, None, 46, 562, 564, '>99'),
			
            (150, None, None, 68, None, 559, 561, '>99'),
            (149, 67, 66, None, None, 556, 558, '>99'),
            (148, None, None, 67, None, 552, 555, '>99'),
            (147, 66, 65, None, 45, 549, 551, '>99'),
            (146, None, None, 66, None, 546, 548, '>99'),
			
            (145, 65, 64, None, None, 543, 545, '>99'),
            (144, None, None, 65, 44, 540, 542, '>99'),
            (143, None, None, None, None, 536, 539, '>99'),
            (142, 64, 63, 64, None, 533, 535, '>99'),
            (141, None, None, None, 43, 530, 532, '>99'),
			
            (140, 63, 62, None, None, 527, 529, '>99'),
            (139, None, None, 63, None, 523, 526, '>99'),
            (138, 62, 61, None, 42, 520, 522, 99),
            (137, None, None, 62, None, 517, 519, 99),
            (136, 61, None, None, None, 514, 516, 99),
			
            (135, None, 60, 61, None, 511, 513, 99),
            (134, None, None, None, 41, 507, 510, 99),
            (133, 60, 59, 60, None, 504, 506, 99),
            (132, None, None, None, None, 501, 503, 98),
            (131, 59, 58, 59, 40, 498, 500, 98),
			
            (130, None, None, None, None, 494, 497, 98),
            (129, 58, None, 58, None, 491, 493, 97),
            (128, None, 57, None, 39, 488, 490, 97),
            (127, 57, None, None, None, 485, 487, 96),
            (126, None, 56, 57, None, 482, 484, 96),
			
            (125, None, None, None, 38, 478, 480, 95),
            (124, 56, 55, 56, None, 475, 477, 95),
            (123, None, None, None, None, 472, 474, 94),
            (122, 55, None, 55, None, 469, 471, 93),
            (121, None, 54, None, 37, 465, 468, 92),
			
            (120, 54, None, 54, None, 462, 464, 91),
            (119, None, 53, None, None, 459, 461, 90),
            (118, 53, None, 53, 36, 456, 458, 88),
            (117, None, 52, None, None, 452, 455, 87),
            (116, None, None, 52, None, 449, 451, 86),
			
            (115, 52, None, None, 35, 446, 448, 84),
            (114, None, 51, None, None, 443, 445, 82),
            (113, 51, None, 51, None, 440, 442, 81),
            (112, None, 50, None, 34, 436, 439, 79),
            (111, 50, None, 50, None, 433, 435, 77),
			
            (110, None, 49, None, None, 430, 432, 75),
            (109, None, None, 49, 33, 427, 429, 73),
            (108, 49, None, None, None, 424, 426, 70),
            (107, None, 48, 48, None, 420, 423, 68),
            (106, 48, None, None, None, 417, 419, 66),
			
            (105, None, 47, 47, 32, 414, 416, 63),
            (104, 47, None, None, None, 411, 413, 61),
            (103, None, 46, 46, None, 407, 410, 58),
            (102, 44, None, None, 31, 404, 406, 55),
            (101, None, None, None, None, 401, 403, 53),
			
            (100, None, 45, 45, None, 398, 400, 50),
            (99, 45, None, None, 30, 395, 397, 47),
            (98, None, 44, 44, None, 391, 394, 45),
            (97, 44, None, None, None, 388, 390, 42),
            (96, None, 43, 43, 29, 385, 387, 39),
			
            (95, 43, None, None, None, 382, 384, 37),
            (94, None, None, 42, None, 379, 381, 34),
            (93, 42, 42, None, None, 375, 378, 32),
            (92, None, None, 41, 28, 372, 374, 30),
            (91, None, 41, None, None, 369, 371, 27),
			
            (90, 41, None, 40, None, 366, 368, 25),
            (89, None, 40, None, 27, 362, 365, 23),
            (88, 40, None, None, None, 359, 361, 21),
            (87, None, 39, 39, None, 356, 358, 19),
            (86, None, None, None, 26, 353, 355, 18),
			
            (85, None, None, 38, None, 350, 352, 16),
            (84, 38, 38, None, None, 346, 349, 14),
            (83, None, None, 37, 25, 343, 345, 13),
            (82, None, 37, None, None, 340, 342, 12),
            (81, 37, None, 36, None, 337, 339, 10),
			
            (80, None, 36, None, None, 333, 336, 9),
            (79, 36, None, 35, 24, 330, 332, 8),
            (78, None, None, None, None, 327, 329, 7),
            (77, 35, 35, 34, None, 324, 326, 6),
            (76, None, None, None, 23, 321, 323, 5),
			
            (75, 34, 34, None, None, 317, 320, 5),
            (74, None, None, 33, None, 314, 316, 4),
            (73, None, 33, None, 22, 311, 313, 4),
            (72, 33, None, 32, None, 308, 310, 3),
            (71, None, None, None, None, 304, 307, 3),
			
            (70, 32, 32, 31, 21, 301, 303, 2),
            (69, None, None, None, 20, 298, 300, 2),
            (68, 31, 31, 30, None, 295, 297, 2),
            (67, None, None, None, None, 292, 294, 1),
            (66, None, 30, 29, 20, 288, 291, 1),
			
            (65, 30, None, None, None, 285, 287, 1),
            (64, None, None, 28, None, 282, 284, 1),
            (63, 29, 29, None, 19, 279, 281, '<1'),
            (62, None, None, None ,None, 276, 278, '<1'),
            (61, 28, 28, 27, None, 272, 275, '<1'),
			
            (60, None, None, None, 18, 269, 271, '<1'),
            (59, 27, 27, 26, None, 266, 268, '<1'),
            (58, None, None, None, None, 263, 265, '<1'),
            (57, None, None, 25, 17, 259, 262, '<1'),
            (56, 26, 26, None, None, 256, 258, '<1'),
			
            (55, None, None, 24, None, 253, 255, '<1'),
            (54, 25, 25, None, None, 250, 252, '<1'),
            (53, None, None, 23, 16, 246, 249, '<1'),
            (52, 24, 24, None, None, 243, 245, '<1'),
            (51, None, None, 22, None, 240, 242, '<1'),
			
            (50, 23, None, None, 15, 237, 239, '<1'),
            (49, None, 23, None, None, 234, 236, '<1'),
            (48, None, None, 21, None, 230, 232, '<1'),
            (47, None, 22, None, 14, 227, 229, '<1'),
            (46, 19, None, None, None, 224, 226, '<1'),
			
            (45, 21, 21, None, None, 220, 223, '<1'),
            (44, None, None, 19, 13, 217, 219, '<1'),
            (43, 20, None, None, None, 214, 216, '<1'),
            (42, None, 20, 18, None, 211, 213, '<1'),
            (41, 19, None, None, None, 207, 210, '<1'),
			
            (40, None, 19, 17, 12, 205, 206, '<1'),
            (39, None, None, None, None, 201, 203, '<1'),
            (38, 18, 18, 16, None, 198, 200, '<1'),
            (37, None, None, None, 11, 195, 197, '<1'),
            (36, 17, None, None, None, 192, 194, '<1'),
			
            (35, None, 17, 15, None, 188, 190, '<1'),
            (34, 16, None, None, 10, 185, 187, '<1'),
            (33, None, 16, 14, None, 182, 184, '<1'),
            (32, 12, 12, 11, None, 179, 181, '<1'),
            (31, None, 15, 13, 9, 176, 178, '<1'),
			
            (30, None, None, None, None, 172, 175, '<1'),
            (29, 14, None, 12, None, 169, 171, '<1'),
            (28, None, 14, None, None, 166, 168, '<1'),
            (27, None, None, 11, 8, 162, 164, '<1'),
            (26, None, 13, None, None, 159, 161, '<1'),
			
            (25, 12, None, None, None, 156, 158, '<1'),
            (24, None, 12, None, 7, 152, 154, '<1'),
            (23, None, None, None, None, 149, 151, '<1'),
            (22, 11, None, 9, None, 146, 148, '<1'),
            (21, None, 11, None, 6, 143, 145, '<1'),
            (20, "3-10", "3-10", "3-8", "2-5", 80, 142, '<1')
        ]
        # Suppression des anciennes données pour la tranche 3-6 ans
        NoteDomaineVMapping.objects.filter(tranche_age='3-6').delete()

        # Import des nouvelles données
        for mapping in mappings_3_6_ans:
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
                    tranche_age='3-6',
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
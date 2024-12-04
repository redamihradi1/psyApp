from django.core.management.base import BaseCommand
from vineland.models import NoteDomaineVMapping

class Command(BaseCommand):
    help = 'Import des données de correspondance pour la tranche 3-6 ans'

    def handle(self, *args, **options):
        mappings_3_6_ans = [
            # Format: (note_standard, comm, vie_quot, social, motric, note_comp_min, note_comp_max, rang)
            (160, 72, "71-72", 72, None, 591, 640, '>99'),
            (159, None, 70, None, None, 588, 590, '>99'),
            (158, 71, None, None, None, 585, 587, '>99'),
            (157, None, 69, 71, None, 581, 584, '>99'),
            (156, 70, None, None, None, 578, 580, '>99'),
            (155, None, 68, 70, None, 575, 577, '>99'),
            (154, 69, None, None, None, 572, 574, '>99'),
            (153, None, 67, 69, None, 569, 571, '>99'),
            (152, None, None, None, 46, 565, 568, '>99'),
            (151, 68, None, 68, None, 562, 564, '>99'),
            (150, None, 66, None, None, 559, 561, '>99'),
            (149, 67, None, 67, None, 556, 558, '>99'),
            (148, None, None, None, 45, 552, 555, '>99'),
            (147, 66, 65, 66, None, 549, 551, '>99'),
            (146, None, None, None, None, 546, 548, '>99'),
            (145, 65, 64, 65, 44, 543, 545, '>99'),
            (144, None, None, None, None, 540, 542, '>99'),
            (143, None, 63, 64, None, 536, 539, '>99'),
            (142, 64, None, None, None, 533, 535, '>99'),
            (141, None, 62, None, 43, 530, 532, '>99'),
            (140, 63, None, 63, None, 527, 529, '>99'),
            (139, None, 61, None, None, 523, 526, '>99'),
            (138, 62, None, 62, 42, 520, 522, 99),
            (137, 61, None, None, None, 517, 519, 99),
            (136, None, 60, 61, None, 514, 516, 99),
            (135, None, None, None, 41, 511, 513, 99),
            (134, 60, 59, 60, None, 507, 510, 99),
            (133, None, None, None, None, 504, 506, 99),
            (132, 59, 58, 59, 40, 501, 503, 98),
            (131, None, None, None, None, 498, 500, 98),
            (130, 58, 57, 58, None, 494, 497, 98),
            (129, None, None, None, 39, 491, 493, 97),
            (128, 57, 56, 57, None, 488, 490, 97),
            (127, None, None, None, None, 485, 487, 96),
            (126, None, None, None, 38, 481, 484, 96),
            (125, 56, 55, 56, None, 478, 480, 95),
            (124, None, None, None, None, 475, 477, 95),
            (123, 55, None, 55, None, 472, 474, 94),
            (122, None, 54, None, 37, 469, 471, 93),
            (121, None, None, 54, None, 465, 468, 92),
            (120, 54, 53, None, None, 462, 464, 91),
            (119, None, None, 53, 36, 459, 461, 90),
            (118, 53, 52, None, None, 456, 458, 88),
            (117, None, None, None, None, 452, 455, 87),
            (116, None, None, 52, 35, 449, 451, 86),
            (115, 52, None, None, None, 446, 448, 84),
            (114, None, 51, 51, None, 443, 445, 82),
            (113, 51, None, None, 34, 440, 442, 81),
            (112, None, 50, 50, None, 436, 439, 79),
            (111, 50, None, None, None, 433, 435, 77),
            (110, None, 49, 49, 33, 430, 432, 75),
            (109, 49, None, None, None, 427, 429, 73),
            (108, None, 48, 48, None, 424, 426, 70),
            (107, 48, None, None, 32, 420, 423, 68),
            (106, None, 47, 47, None, 417, 419, 66),
            (105, 47, None, None, None, 414, 416, 63),
            (104, None, 46, 46, 31, 410, 413, 61),
            (103, 46, None, None, None, 407, 409, 58),
            (102, None, None, None, None, 404, 406, 55),
            (101, None, 45, 45, 30, 401, 403, 53),
            (100, 45, None, None, None, 398, 400, 50),
            (99, None, 44, 44, None, 395, 397, 47),
            (98, 44, None, None, 29, 391, 394, 45),
            (97, None, 43, 43, None, 388, 390, 42),
            (96, 43, None, None, None, 385, 387, 39),
            (95, None, None, 42, 28, 382, 384, 37),
            (94, 42, 42, None, None, 379, 381, 34),
            (93, None, None, 41, None, 375, 378, 32),
            (92, None, None, None, None, 372, 374, 30),
            (91, 41, 41, None, 28, 369, 371, 27),
            (90, 41, None, None, None, 366, 368, 25),
            (89, None, 40, None, 27, 362, 365, 23),
            (88, None, None, 40, None, 359, 361, 21),
            (87, 39, None, 39, None, 356, 358, 19),
            (86, None, None, None, 26, 353, 355, 18),
            (85, None, 38, 38, None, 350, 352, 16),
            (84, 38, None, None, None, 346, 349, 14),
            (83, None, 37, 37, 25, 343, 345, 13),
            (82, 37, None, 36, None, 340, 342, 12),
            (81, None, 36, None, None, 337, 339, 10),
            (80, 36, None, 35, 24, 333, 336, 9),
            (79, None, None, None, None, 330, 332, 8),
            (78, 35, 35, 34, None, 327, 329, 7),
            (77, None, None, None, 23, 324, 326, 6),
            (76, 34, 34, 33, None, 321, 323, 5),
            (75, None, None, None, None, 317, 320, 5),
            (74, 33, 33, 32, 22, 314, 316, 4),
            (73, None, None, None, None, 311, 313, 4),
            (72, 32, 32, 31, 21, 308, 310, 3),
            (71, None, None, None, None, 304, 307, 3),
            (70, 31, 31, 30, None, 301, 303, 2),
            (69, None, None, None, 20, 298, 300, 2),
            (68, 30, 30, 29, None, 295, 297, 2),
            (67, None, None, None, None, 292, 294, 1),
            (66, 29, 29, 28, 19, 288, 291, 1),
            (65, None, None, None, None, 285, 287, 1),
            (64, 28, 28, 27, None, 282, 284, 1),
            (63, None, None, None, 18, 279, 281, '<1'),
            (62, 27, 27, 26, None, 276, 278, '<1'),
            (61, None, None, None, None, 272, 275, '<1'),
            (60, 26, 26, 25, 17, 269, 271, '<1'),
            (59, None, None, None, None, 266, 268, '<1'),
            (58, 25, 25, 24, None, 263, 265, '<1'),
            (57, None, None, None, 16, 259, 262, '<1'),
            (56, 24, 24, 23, None, 256, 258, '<1'),
            (55, None, None, None, None, 253, 255, '<1'),
            (54, 23, 23, 22, 15, 250, 252, '<1'),
            (53, None, None, None, None, 246, 249, '<1'),
            (52, 22, 22, 21, None, 243, 245, '<1'),
            (51, None, None, None, 14, 240, 242, '<1'),
            (50, 21, 21, 20, None, 237, 239, '<1'),
            (49, None, None, None, None, 233, 236, '<1'),
            (48, 20, 20, 19, 13, 230, 232, '<1'),
            (47, None, None, None, None, 227, 229, '<1'),
            (46, 19, 19, 18, None, 224, 226, '<1'),
            (45, None, None, None, 12, 220, 223, '<1'),
            (44, 18, 18, 17, None, 217, 219, '<1'),
            (43, None, None, None, None, 214, 216, '<1'),
            (42, 17, 17, 16, 11, 211, 213, '<1'),
            (41, None, None, None, None, 207, 210, '<1'),
            (40, 16, 16, 15, None, 204, 206, '<1'),
            (39, None, None, None, 10, 201, 203, '<1'),
            (38, 15, 15, 14, None, 198, 200, '<1'),
            (37, None, None, None, None, 194, 197, '<1'),
            (36, 14, 14, 13, 9, 191, 193, '<1'),
            (35, None, None, None, None, 188, 190, '<1'),
            (34, 13, 13, 12, None, 185, 187, '<1'),
            (33, None, None, None, 8, 181, 184, '<1'),
            (32, 12, 12, 11, None, 178, 180, '<1'),
            (31, None, None, None, None, 175, 177, '<1'),
            (30, 11, 11, 10, 7, 172, 174, '<1'),
            (29, None, None, None, None, 168, 171, '<1'),
            (28, 10, 10, 9, None, 165, 167, '<1'),
            (27, None, None, None, 6, 162, 164, '<1'),
            (26, 9, 9, 8, None, 159, 161, '<1'),
            (25, None, None, None, None, 155, 158, '<1'),
            (24, 8, 8, 7, 5, 152, 154, '<1'),
            (23, None, None, None, None, 149, 151, '<1'),
            (22, 7, 7, 6, None, 146, 148, '<1'),
            (21, None, None, None, None, 143, 145, '<1'),
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
from django.core.management.base import BaseCommand
from vineland.models import NoteDomaineVMapping  # Ajustez le chemin d'import selon votre structure

class Command(BaseCommand):
    help = 'Import des données de correspondance pour la tranche 1-2 ans'

    def handle(self, *args, **options):
        # Format: (note_standard, comm, vie_quot, social, motric, note_comp_min, note_comp_max, rang)
        mappings_1_2_ans = [
                            (160, None, "69-72", 72, None, 585, 640, '>99'),
                            (159, None, None, None, None, 582, 584, '>99'),
                            (158, None, 68, 71, None, 579, 581, '>99'),
                            (157, None, None, None, None, 576, 578, '>99'),
                            (156, 48, None, 70, None, 573, 575, '>99'),
                            
                            (155, None, 67, None, None, 569, 572, '>99'),
                            (154, None, None, None, 48, 566, 568, '>99'),
                            (153, 47, 66, 69, None, 563, 565, '>99'),
                            (152, None, None, None, None, 560, 562, '>99'),
                            (151, None, None, 68, 47, 557, 559, '>99'),
                            
                            (150, 46, 65, None, None, 554, 556, '>99'),
                            (149, None, None, 67, None, 551, 553, '>99'),
                            (148, None, None, None, 46, 548, 550, '>99'),
                            (147, 45, 64, 66, None, 545, 547, '>99'),
                            (146, None, None, None, None, 542, 544, '>99'),
                            
                            (145, None, 63, None, 45, 538, 541, '>99'),
                            (144, 44, None, 65, None, 535, 537, '>99'),
                            (143, None, None, None, None, 532, 534, '>99'),
                            (142, None, 62, 64, 44, 529, 531, '>99'),
                            (141, 43, None, None, None, 526, 528, '>99'),
                            
                            (140, None, 61, 63, None, 523, 525, '>99'),
                            (139, None, None, None, 43, 520, 522, '>99'),
                            (138, None, None, 62, None, 517, 519, 99),
                            (137, 42, 60, None, None, 514, 516, 99),
                            (136, None, None, 61, 42, 511, 513, 99),
                            
                            (135, None, 59, None, None, 508, 510, 99),
                            (134, 41, None, None, None, 504, 507, 99),
                            (133, None, None, 60, 41, 501, 503, 99),
                            (132, None, 58, None, None, 498, 500, 98),
                            (131, 40, None, 59, None, 495, 497, 98),
                            
                            (130, None, 57, None, 40, 492, 494, 98),
                            (129, None, None, 58, None, 489, 491, 97),
                            (128, 39, None, None, None, 486, 488, 97),
                            (127, None, 56, 57, 39, 483, 485, 97),
                            (126, None, None, None, None, 480, 482, 96),
                            
                            (125, 38, None, None, None, 477, 479, 95),
                            (124, None, 55, 56, 38, 473, 476, 95),
                            (123, None, None, None, None, 470, 472, 94),
                            (122, 37, 54, 55, None, 467, 469, 93),
                            (121, None, None, None, 37, 464, 466, 92),
                            
                            (120, None, None, 54, None, 461, 463, 91),
                            (119, 36, 53, None, None, 458, 460, 90),
                            (118, None, None, 53, 36, 455, 457, 88),
                            (117, None, 52, None, None, 452, 454, 87),
                            (116, 35, None, None, None, 449, 451, 85),
                            
                            (115, None, None, 52, 35, 446, 448, 84),
                            (114, None, 51, None, None, 443, 445, 82),
                            (113, 34, None, 51, None, 439, 442, 81),
                            (112, None, 50, None, 34, 436, 438, 79),
                            (111, None, None, 50, None, 433, 435, 77),
                            
                            (110, 33, None, None, None, 430, 432, 75),
                            (109, None, 49, 49, 33, 427, 429, 73),
                            (108, None, None, None, None, 424, 426, 70),
                            (107, 32, None, None, None, 421, 423, 68),
                            (106, None, 48, 48, 32, 418, 420, 66),
                            
                            (105, None, None, None, None, 415, 417, 63),
                            (104, None, 47, 47, None, 412, 414, 61),
                            (103, 31, None, None, 31, 408, 411, 58),
                            (102, None, None, 46, None, 405, 407, 55),
                            (101, None, 46, None, None, 402, 404, 53),
                            
                            (100, 30, None, 45, 30, 399, 401, 50),
                            (99, None, 45, None, None, 396, 398, 47),
                            (98, None, None, 41, None, 393, 395, 45),
                            (97, 29, None, 44, 29, 390, 392, 42),
                            (96, None, 44, None, None, 387, 389, 39),
                            
                            (95, None, None, 43, None, 384, 386, 37),
                            (94, 28, 43, None, 28, 381, 383, 34),
                            (93, None, None, 42, None, 378, 380, 32),
                            (92, None, None, None, None, 374, 377, 30),
                            (91, 27, 42, 41, 27, 371, 373, 27),
                            
                            (90, None, None, None, None, 368, 370, 25),
                            (89, None, 41, None, None, 365, 367, 23),
                            (88, 26, None, 40, 26, 362, 364, 21),
                            (87, None, None, None, None, 359, 361, 19),
                            (86, None, 40, 39, None, 356, 358, 18),
                            
                            (85, 25, None, None, None, 353, 355, 16),
                            (84, None, None, 38, None, 350, 352, 14),
                            (83, None, 39, None, None, 347, 349, 13),
                            (82, 24, None, 37, 24, 343, 346, 12),
                            (81, None, 38, None, None, 340, 342, 10),
                            
                            (80, None, None, None, None, 337, 339, 9),
                            (79, 23, None, 36, 23, 334, 336, 8),
                            (78, None, 37, None, None, 331, 333, 7),
                            (77, None, None, 35, None, 328, 330, 6),
                            (76, 22, 36, None, 22, 325, 327, 5),
                            
                            (75, None, None, 34, None, 322, 324, 5),
                            (74, None, None, None, None, 319, 321, 4),
                            (73, 21, 35, 33, 21, 316, 318, 4),
                            (72, None, None, None, None, 313, 315, 3),
                            (71, None, 34, 32, None, 309, 312, 3),
                            
                            (70, None, None, None, 20, 306, 308, 2),
                            (69, 20, None, None, None, 303, 305, 2),
                            (68, None, 33, 31, None, 300, 302, 2),
                            (67, None, None, None, 19, 297, 299, 1),
                            (66, 19, None, 30, None, 294, 296, 1),
                            
                            (65, None, 32, None, None, 291, 293, 1),
                            (64, None, None, 29, 18, 288, 290, 1),
                            (63, 18, 31, None, None, 285, 287, 1),
                            (62, None, None, 28, None, 282, 284, 1),
                            (61, None, None, None, 17, 278, 281, '<1'),
                            
                            (60, 17, 30, None, None, 275, 277, '<1'),
                            (59, None, None, 27, None, 272, 274, '<1'),
                            (58, None, 29, None, 16, 269, 271, '<1'),
                            (57, 16, None, 26, None, 266, 268, '<1'),
                            (56, None, None, None, None, 263, 265, '<1'),
                            
                            (55, None, 28, 25, 15, 260, 262, '<1'),
                            (54, 15, None, None, None, 257, 259, '<1'),
                            (53, None, 27, 24, None, 254, 256, '<1'),
                            (52, None, None, None, 14, 251, 253, '<1'),
                            (51, 14, None, None, None, 248, 250, '<1'),
                            
                            (50, None, 26, 23, None, 244, 247, '<1'),
                            (49, None, None, None, 13, 241, 243, '<1'),
                            (48, 13, 25, 22, None, 238, 240, '<1'),
                            (47, None, None, None, None, 235, 237, '<1'),
                            (46, None, None, 21, 12, 232, 234, '<1'),
                            
                            (45, 12, 24, None, None, 229, 231, '<1'),
                            (44, None, None, 20, None, 226, 228, '<1'),
                            (43, None, None, None, 11, 223, 225, '<1'),
                            (42, 11, 23, None, None, 220, 222, '<1'),
                            (41, None, None, 19, None, 217, 219, '<1'),
                            
                            (40, None, 22, None, 10, 213, 216, '<1'),
                            (39, 10, None, 18, None, 210, 212, '<1'),
                            (38, None, None, None, None, 207, 209, '<1'),
                            (37, None, 21, 17, 9, 204, 206, '<1'),
                            (36, None, None, None, None, 201, 203, '<1'),
                            
                            (35, 9, 20, 16, None, 198, 200, '<1'),
                            (34, None, None, None, 8, 195, 197, '<1'),
                            (33, None, None, None, None, 192, 194, '<1'),
                            (32, 8, 19, 15, None, 189, 191, '<1'),
                            (31, None, None, None, 7, 186, 188, '<1'),
                            
                            (30, None, 18, 14, None, 183, 184, '<1'),
                            (29, 7, None, None, None, 179, 182, '<1'),
                            (28, None, None, 13, 6, 176, 178, '<1'),
                            (27, None, 17, None, None, 173, 175, '<1'),
                            (26, 6, None, 12, None, 170, 172, '<1'),
                            
                            (25, None, 16, None, 5, 167, 169, '<1'),
                            (24, None, None, None, None, 164, 166, '<1'),
                            (23, 5, None, 11, None, 161, 163, '<1'),
                            (22, None, 15, None, 4, 158, 160, '<1'),
                            (21, None, None, 10, None, 155, 157, '<1'),
                            (20, "2-4", "3-14", "3-9", "2-3", 80, 154, '<1')
                        ]

        # Suppression des anciennes données pour la tranche 1-2 ans
        NoteDomaineVMapping.objects.filter(tranche_age='1-2').delete()

        # Import des nouvelles données
        for mapping in mappings_1_2_ans:
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
                    tranche_age='1-2',
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
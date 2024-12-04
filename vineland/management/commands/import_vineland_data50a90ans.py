from django.core.management.base import BaseCommand
from vineland.models import NoteDomaineVMapping

class Command(BaseCommand):
    help = 'Import des données de correspondance pour la tranche 50-90 ans'

    def handle(self, *args, **options):
        mappings_50_90_ans = [
            # Format: (note_standard, comm, vie_quot, social, motric, note_comp_min, note_comp_max, rang)
            (160, None, None, None, None, None, None, '>99'),
            (159, None, None, None, None, None, None, '>99'),
            (158, None, None, None, None, None, None, '>99'),
            (157, None, None, None, None, None, None, '>99'),
            (156, None, None, None, None, None, None, '>99'),
            (155, None, None, None, None, None, None, '>99'),
            (154, None, None, None, None, None, None, '>99'),
            (153, None, None, None, None, None, None, '>99'),
            (152, None, None, None, None, None, None, '>99'),
            (151, None, None, None, None, None, None, '>99'),
            (150, None, None, None, None, None, None, '>99'),
            (149, None, None, None, None, None, None, '>99'),
            (148, None, None, None, None, None, None, '>99'),
            (147, None, None, None, None, None, None, '>99'),
            (146, None, None, None, None, None, None, '>99'),
            (145, None, None, None, None, None, None, '>99'),
            (144, None, None, None, None, None, None, '>99'),
            (143, None, None, None, None, None, None, '>99'),
            (142, None, None, None, None, None, None, '>99'),
            (141, None, None, None, None, None, None, '>99'),
            (140, None, None, None, None, None, None, '>99'),
            (139, None, None, None, None, None, None, '>99'),
            (138, None, None, None, None, None, None, 99),
            (137, None, None, None, None, None, None, 99),
            (136, None, None, None, None, None, None, 99),
            (135, None, None, None, None, None, None, 99),
            (134, None, None, None, None, None, None, 99),
            (133, None, None, None, None, None, None, 99),
            (132, None, None, None, None, None, None, 98),
            (131, None, None, None, None, None, None, 98),
            (130, None, None, None, None, None, None, 98),
            (129, None, None, None, None, None, None, 97),
            (128, None, None, None, None, None, None, 97),
            (127, None, None, None, None, None, None, 96),
            (126, None, None, None, None, None, None, 96),
            (125, None, None, None, None, 358, 358, 95),
            (124, None, 54, None, None, 356, 357, 95),
            (123, None, None, None, None, 354, 355, 94),
            (122, None, 53, None, None, 351, 353, 93),
            (121, None, None, 51, None, 349, 350, 92),
            (120, None, 52, 50, None, 347, 348, 91),
            (119, None, None, None, None, 344, 346, 90),
            (118, None, 51, 49, None, 342, 343, 88),
            (117, None, None, None, None, 340, 341, 87),
            (116, None, 50, 48, None, 338, 339, 86),
            (115, None, None, None, None, 335, 337, 84),
            (114, 49, 50, 48, 33, 333, 334, 82),
            (113, None, 49, 47, None, 330, 332, 81),
            (112, 48, None, None, None, 328, 329, 79),
            (111, None, 48, 46, 32, 326, 327, 77),
            (110, 47, None, None, None, 324, 325, 75),
            (109, None, 47, 45, None, 322, 323, 73),
            (108, None, None, None, 31, 319, 321, 70),
            (107, 46, 46, 44, None, 317, 318, 68),
            (106, None, None, None, None, 315, 316, 66),
            (105, 45, 45, 43, 30, 312, 314, 63),
            (104, None, None, None, None, 309, 311, 61),
            (103, None, 44, 42, None, 306, 308, 58),
            (102, 44, None, None, None, 303, 305, 55),
            (101, None, None, 41, 29, 301, 302, 53),
            (100, 43, 43, None, None, 299, 300, 50),
            (99, None, None, 40, None, 296, 298, 47),
            (98, None, 42, None, 28, 294, 295, 45),
            (97, 42, None, 39, None, 292, 293, 42),
            (96, 41, 41, None, None, 289, 291, 39),
            (95, None, None, 38, None, 287, 288, 37),
            (94, 40, 40, None, None, 284, 286, 34),
            (93, None, None, None, 27, 282, 283, 32),
            (92, None, None, None, None, 280, 281, 30),
            (91, 40, None, 38, 28, 278, 279, 27),
            (90, None, 40, 37, None, 276, 277, 25),
            (89, None, None, None, 27, 273, 275, 23),
            (88, 39, 39, 36, None, 271, 272, 21),
            (87, None, None, 35, None, 269, 270, 19),
            (86, 38, 38, None, None, 266, 268, 18),
            (85, None, None, 34, 26, 264, 265, 16),
            (84, None, 37, None, None, 262, 263, 14),
            (83, 37, None, 33, None, 260, 261, 13),
            (82, None, 36, None, None, 257, 259, 12),
            (81, 36, None, 32, 25, 255, 256, 10),
            (80, None, 35, None, None, 253, 254, 9),
            (79, None, None, 31, None, 250, 252, 8),
            (78, 35, 34, None, 24, 248, 249, 7),
            (77, None, None, 30, None, 246, 247, 6),
            (76, 34, 33, 29, None, 243, 245, 5),
            (75, None, None, None, None, 241, 242, 4),
            (74, 33, 32, 28, 23, 239, 240, 4),
            (73, None, None, None, None, 237, 238, 3),
            (72, 32, 31, 27, 22, 234, 236, 3),
            (71, None, None, None, None, 232, 233, 3),
            (70, 31, 30, 26, None, 229, 231, 2),
            (69, None, None, None, 21, 227, 229, 2),
            (68, 30, 29, 25, None, 225, 226, 2),
            (67, None, None, None, None, 223, 224, 1),
            (66, 29, 28, 24, 20, 221, 222, 1),
            (65, None, None, None, None, 218, 220, 1),
            (64, 28, 27, 23, None, 216, 217, 1),
            (63, None, None, None, None, 214, 215, 1),
            (62, 27, 26, 22, 19, 211, 213, '<1'),
            (61, None, None, None, None, 209, 210, '<1'),
            (60, 26, 25, 21, 18, 207, 208, '<1'),
            (59, None, None, None, None, 204, 206, '<1'),
            (58, 25, 24, 20, None, 202, 203, '<1'),
            (57, None, None, None, 17, 200, 201, '<1'),
            (56, 24, 23, 19, None, 198, 199, '<1'),
            (55, None, None, None, None, 195, 197, '<1'),
            (54, 23, 22, 18, 16, 193, 194, '<1'),
            (53, None, None, None, None, 191, 192, '<1'),
            (52, 22, 21, 17, None, 188, 190, '<1'),
            (51, None, None, None, 15, 186, 187, '<1'),
            (50, 21, 20, 16, None, 184, 185, '<1'),
            (49, None, None, None, None, 181, 183, '<1'),
            (48, 20, 19, 15, 14, 179, 180, '<1'),
            (47, None, None, None, None, 177, 178, '<1'),
            (46, 19, 18, 14, None, 175, 176, '<1'),
            (45, None, None, None, 13, 172, 174, '<1'),
            (44, 18, 17, 13, None, 170, 171, '<1'),
            (43, None, None, None, None, 168, 169, '<1'),
            (42, 17, 16, 12, 12, 165, 167, '<1'),
            (41, None, None, None, None, 163, 164, '<1'),
            (40, 16, 15, 11, None, 161, 162, '<1'),
            (39, None, None, None, 11, 159, 160, '<1'),
            (38, 15, 14, 10, None, 156, 158, '<1'),
            (37, None, None, None, None, 154, 155, '<1'),
            (36, 14, 13, 9, 10, 152, 153, '<1'),
            (35, None, None, None, None, 149, 151, '<1'),
            (34, 13, 12, 8, None, 147, 148, '<1'),
            (33, None, None, None, 9, 145, 146, '<1'),
            (32, 12, 11, 7, None, 142, 144, '<1'),
            (31, None, None, None, None, 140, 141, '<1'),
            (30, 11, 10, 6, 8, 138, 139, '<1'),
            (29, None, None, None, None, 135, 137, '<1'),
            (28, 10, 9, 5, None, 133, 134, '<1'),
            (27, None, None, None, 7, 131, 132, '<1'),
            (26, 9, 8, 4, None, 129, 130, '<1'),
            (25, None, None, None, None, 126, 128, '<1'),
            (24, 8, 7, 3, 6, 124, 125, '<1'),
            (23, None, None, None, None, 122, 123, '<1'),
            (22, 7, 6, None, 5, 119, 121, '<1'),
            (21, None, None, None, None, 119, 121, '<1'),
            (20, "3-12", "3-11", "3-4", "2-10", 60, 118, '<1')
        ]

        # Suppression des anciennes données pour la tranche 50-90 ans
        NoteDomaineVMapping.objects.filter(tranche_age='50-90').delete()

        # Import des nouvelles données
        for mapping in mappings_50_90_ans:
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
                    tranche_age='50-90',
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
                'Import réussi des données pour la tranche 19-49 ans'
            )
        )
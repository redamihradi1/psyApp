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
            (122, None, None, None, None, 351, 353, 93),
            (121, None, 53, None, None, 349, 350, 92),
			
            (120, None, None, 51, None, 347, 348, 91),
            (119, None, 52, None, None, 344, 346, 90),
            (118, None, None, 50, None, 342, 343, 88),
            (117, None, 51, None, None, 340, 341, 87),
            (116, None, None, 49, None, 338, 339, 86),
			
            (115, None, None, None, None, 335, 337, 84),
            (114, 49, 50, 48,None , 333, 334, 82),
            (113, None, None, None, 33, 330, 332, 81),
            (112, 48, None, None, None, 328, 329, 79),
            (111, 48, None, None, None, 326, 327, 77),
			
            (110, None, None, None, None, 324, 325, 75),
            (109, 47, 48, 46, 32, 322, 323, 73),
            (108, None, None, None, None, 319, 321, 70),
            (107, None, 47, 45, None, 317, 318, 68),
            (106, 46, None, None, None, 315, 316, 66),
			
            (105, None, 46, 44, 31, 312, 314, 63),
            (104, 45, None, None, None, 309, 311, 61),
            (103, None, None, 43, None, 306, 308, 58),
            (102, None, 45, None, None, 305, 307, 55),
            (101, 44, None, 42, 30, 303, 304, 53),
			
            (100, None, 44, None, None, 301, 302, 50),
            (99, 43, None, 41, None, 299, 300, 47),
            (98, None, None, None, None, 296, 298, 45),
            (97, None, 43, 40, 29, 294, 295, 42),
            (96, 42, None, None, None, 292, 293, 39),
			
            (95, None, None, 38, None, 289, 291, 37),
            (94, 40, 40, None, None, 287, 288, 34),
            (93, None, None, None, 27, 285, 286, 32),
            (92, None, None, None, None, 282, 284, 30),
            (91, 40, None, 38, 28, 280, 281, 27),
			
            (90, None, 40, 37, None, 278, 279, 25),
            (89, None, None, None, 27, 276, 277, 23),
            (88, 39, 39, 39, 27, 273, 275, 21),
            (87, None, None, None, None, 271, 272, 19),
            (86, 38, None, 35, None, 269, 270, 18),
			
            (85, None, 38, None, None, 266, 268, 16),
            (84, None, None, 34, 26, 264, 265, 14),
            (83, 37, None, 33, None, 262, 263, 13),
            (82, None, 36, None, None, 260, 261, 12),
            (81, 36, None, None, None, 257, 259, 10),
			
            (80, None, 36, 32, 25, 255, 256, 9),
            (79, None, None, None, None, 253, 252, 8),
            (78, 35, 35, 31, None, 250, 252, 7),
            (77, None, None, None, None, 248, 249, 6),
            (76, 34, 34, 30, 24, 246, 247, 5),
			
            (75, None, None, None, None, 243, 245, 4),
            (74, None, None, None, None, 241, 242, 4),
            (73, 33, 33, 29, None, 239, 240, 3),
            (72, None, None, None, None, 237, 238, 3),
            (71, None, 32, 28, None, 232, 233, 3),
			
            (70, 32, None, None, None, 232, 233, 2),
            (69, None, None, 27, None, 230, 231, 2),
            (68, 31, 31, None, None, 227, 229, 2),
            (67, None, None, 26, 22, 225, 226, 1),
            (66, None, 30, None, None, 223, 224, 1),
			
            (65, 30, None, 25, None, 221, 222, 1),
            (64, None, 29, None, None, 218, 220, 1),
            (63, 29, None, 24, 21, 216, 217, 1),
            (62, 27, 26, 22, 19, 211, 213, '<1'),
            (61, None, 28, 23, None, 211, 213, '<1'),
			
            (60, 28, None, None, None, 209, 210, '<1'),
            (59, None, 27, 22, 20, 207, 208, '<1'),
            (58, 27, None, None, None, 204, 206, '<1'),
            (57, None, None, None, 17, 202, 203, '<1'),
            (56, None, 26, 21, None, 200, 201, '<1'),
			
            (55, 26, None, None, 19, 198, 199, '<1'),
            (54, None, 25, 20, None, 195, 197, '<1'),
            (53, 25, None, None, None, 193, 194, '<1'),
            (52, None, None, 19, None, 188, 191, '<1'),
            (51, None, 24, None, 18, 188, 190, '<1'),
			
            (50, 24, None, 18, 19, 198, 187, '<1'),
            (49, None, 23, None, None, 184, 185, '<1'),
            (48, None, None, 17, None, 179, 183, '<1'),
            (47, 23, 22, None, 17, 179, 180, '<1'),
            (46, None, None, 16, None, 177, 178, '<1'),
			
            (45, 22, None, None, None, 175, 176, '<1'),
            (44, None, 21, 15, None, 172, 174, '<1'),
            (43, None, None, None, None, 170, 171, '<1'),
            (42, 21, 20, 14, 16, 168, 169, '<1'),
            (41, None, None, None, None, 165, 167, '<1'),
			
            (40, 20, None, 13, None, 163, 164, '<1'),
            (39, None, 19, None, None, 161, 162, '<1'),
            (38, None, None, None, 15, 159, 160, '<1'),
            (37, 19, 18, 12, None, 156, 158, '<1'),
            (36, None, None, None, None, 154, 155, '<1'),
			
            (35, 18, 17, 11, None, 152, 153, '<1'),
            (34, None, None, None, 14, 149, 151, '<1'),
            (33, None, None, None, 9, 147, 148, '<1'),
            (32, 17, 16, None, None, 145, 146, '<1'),
            (31, None, None, None, None, 140, 141, '<1'),
			
            (30, 16, 15, None, 13, 140, 141, '<1'),
            (29, None, None, 8, None, 138, 139, '<1'),
            (28, None, None, None, None, 136, 137, '<1'),
            (27, 15, 14, 7, None, 133, 135, '<1'),
            (26, None, None, None, 12, 131, 132, '<1'),
			
            (25, None, 13, 6, None, 129, 130, '<1'),
            (24, 14, None, None, None, 126, 128, '<1'),
            (23, None, 12, 5, None, 124, 125, '<1'),
            (22, 13, None, None, 11, 119, 123, '<1'),
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
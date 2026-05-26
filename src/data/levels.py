LEVELS = {
    1: {
        'name': 'Egypte Antique',
        'rooms': {
            1: {
                'bg': 6,
                'depart': (80, 300),
                'porte': (720, 182),
                'enigmes': [
                    {
                        'id': 'l1r1_hieroglyphes',
                        'x': 240, 'y': 206, 'largeur': 80, 'hauteur': 110,
                        'label': 'Stele aux hieroglyphes',
                        'indice': (
                            "Une stele couverte de symboles egyptiens.\n"
                            "Le cartouche du bas designe la pierre qui permit\n"
                            "de dechiffrer les hieroglyphes. Son nom ?"
                        ),
                        'reponse': 'rosette',
                        'digit_index': 0, 'digit_value': 4,
                        'bijou': 'Scarabee en or',
                    },
                    {
                        'id': 'l1r1_dieu',
                        'x': 1190, 'y': 206, 'largeur': 90, 'hauteur': 130,
                        'label': 'Statue de dieu',
                        'indice': (
                            "Cette statue a une tete de faucon.\n"
                            "Il est le dieu du ciel et du soleil en Egypte.\n"
                            "Son nom en 4 lettres ?"
                        ),
                        'reponse': 'horus',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Oeil d\'Horus en lapis-lazuli',
                    },
                ],
            },
            2: {
                'bg': 7,
                'depart': (80, 300),
                'porte': (760, 158),
                'enigmes': [
                    {
                        'id': 'l1r2_sarcophage',
                        'x': 270, 'y': 150, 'largeur': 90, 'hauteur': 200,
                        'label': 'Sarcophage royal',
                        'indice': (
                            "Le sarcophage porte le nom d un pharaon celebre.\n"
                            "Il construisit la grande pyramide de Gizeh.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'kheops',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Pectoral en or de Kheops',
                    },
                    {
                        'id': 'l1r2_ankh',
                        'x': 1150, 'y': 150, 'largeur': 90, 'hauteur': 200,
                        'label': 'Symbole de vie',
                        'indice': (
                            "Ce symbole egyptien signifie la vie eternelle.\n"
                            "En forme de croix avec une boucle en haut.\n"
                            "Comment s appelle-t-il ?"
                        ),
                        'reponse': 'ankh',
                        'digit_index': 3, 'digit_value': 9,
                        'bijou': 'Croix Ankh en or massif',
                    },
                ],
            },
            3: {
                'bg': 8,
                'depart': (80, 300),
                'porte': (740, 131),
                'enigmes': [
                    {
                        'id': 'l1r3_papyrus',
                        'x': 200, 'y': 163, 'largeur': 90, 'hauteur': 200,
                        'label': 'Rouleau de papyrus',
                        'indice': (
                            "Ce rouleau contient le Livre des Morts egyptien.\n"
                            "Il guidait les ames vers l au-dela.\n"
                            "Combien de chapitres contient-il ? (entre 100 et 200)"
                        ),
                        'reponse': '192',
                        'digit_index': 0, 'digit_value': 3,
                        'bijou': 'Amulette de protection',
                    },
                    {
                        'id': 'l1r3_sphinx',
                        'x': 1130, 'y': 163, 'largeur': 90, 'hauteur': 200,
                        'label': 'Sphinx miniature',
                        'indice': (
                            "Creature mi-homme mi-lion gardienne des pyramides.\n"
                            "Le plus celebre se trouve a Gizeh.\n"
                            "Comment appelle-t-on cette creature ?"
                        ),
                        'reponse': 'sphinx',
                        'digit_index': 1, 'digit_value': 6,
                        'bijou': 'Bague en cornaline du sphinx',
                    },
                ],
            },
            4: {
                'bg': 9,
                'depart': (80, 300),
                'porte': (610, 132),
                'enigmes': [
                    {
                        'id': 'l1r4_ibis',
                        'x': 370, 'y': 188, 'largeur': 90, 'hauteur': 120,
                        'label': 'Statue d ibis',
                        'indice': (
                            "Cet oiseau sacre represente le dieu de la sagesse.\n"
                            "Il est aussi le dieu de l ecriture et de la magie.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'thoth',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Plume de Maat en or',
                    },
                    {
                        'id': 'l1r4_canope',
                        'x': 1050, 'y': 180, 'largeur': 100, 'hauteur': 130,
                        'label': 'Vase canope',
                        'indice': (
                            "Ces vases conservaient les organes des defunts embaumes.\n"
                            "Il y en avait toujours un nombre precis par momie.\n"
                            "Combien ?"
                        ),
                        'reponse': '4',
                        'digit_index': 3, 'digit_value': 1,
                        'bijou': 'Uraeus en jaspe vert',
                    },
                ],
            },
            5: {
                'bg': 10,
                'depart': (80, 300),
                'porte': (1400, 146),
                'enigmes': [
                    {
                        'id': 'l1r5_isis',
                        'x': 210, 'y': 146, 'largeur': 110, 'hauteur': 200,
                        'label': 'Sanctuaire d Isis',
                        'indice': (
                            "Deesse de la magie et de la maternite en Egypte.\n"
                            "Elle ressuscita son epoux Osiris.\n"
                            "Comment s appelle-t-elle ?"
                        ),
                        'reponse': 'isis',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Collier pectoral d Isis',
                    },
                    {
                        'id': 'l1r5_pyramide',
                        'x': 680, 'y': 155, 'largeur': 120, 'hauteur': 160,
                        'label': 'Maquette pyramide',
                        'indice': (
                            "Combien y a-t-il de grandes pyramides a Gizeh ?"
                        ),
                        'reponse': '3',
                        'digit_index': 1, 'digit_value': 0,
                        'bijou': 'Diamant de la pyramide',
                    },
                ],
            },
        },
    },

    2: {
        'name': 'Grece Antique',
        'rooms': {
            1: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l2r1_venus',
                        'x': 700, 'y': 150, 'largeur': 60, 'hauteur': 130,
                        'label': 'Statue sans bras',
                        'indice': (
                            "Cette statue de femme sans bras est l une\n"
                            "des sculptures les plus celebres du Louvre.\n"
                            "Elle represente la deesse grecque de l amour. Son nom ?"
                        ),
                        'reponse': 'aphrodite',
                        'digit_index': 0, 'digit_value': 5,
                        'bijou': 'Collier de perles d Aphrodite',
                    },
                    {
                        'id': 'l2r1_zeus',
                        'x': 1100, 'y': 170, 'largeur': 80, 'hauteur': 110,
                        'label': 'Trident pose',
                        'indice': (
                            "Ce trident appartient au dieu des mers.\n"
                            "Frere de Zeus et d Hades.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'poseidon',
                        'digit_index': 1, 'digit_value': 3,
                        'bijou': 'Trident en argent miniature',
                    },
                ],
            },
            2: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l2r2_amphore',
                        'x': 500, 'y': 200, 'largeur': 70, 'hauteur': 110,
                        'label': 'Amphore peinte',
                        'indice': (
                            "Cette amphore represente des guerriers.\n"
                            "La scene montre le fameux cheval de bois\n"
                            "utilise pour entrer dans une cite. Laquelle ?"
                        ),
                        'reponse': 'troie',
                        'digit_index': 2, 'digit_value': 7,
                        'bijou': 'Fibule en bronze de Troie',
                    },
                    {
                        'id': 'l2r2_olympe',
                        'x': 1000, 'y': 190, 'largeur': 80, 'hauteur': 90,
                        'label': 'Fresque de l Olympe',
                        'indice': (
                            "Combien de dieux principaux habitaient l Olympe\n"
                            "dans la mythologie grecque ?"
                        ),
                        'reponse': '12',
                        'digit_index': 3, 'digit_value': 2,
                        'bijou': 'Medaillon des 12 Olympiens',
                    },
                ],
            },
            3: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l2r3_labyrinthe',
                        'x': 400, 'y': 210, 'largeur': 90, 'hauteur': 80,
                        'label': 'Plan du labyrinthe',
                        'indice': (
                            "Ce plan represente le labyrinthe de Crete.\n"
                            "Il enfermait une creature mi-homme mi-taureau.\n"
                            "Comment s appelait ce monstre ?"
                        ),
                        'reponse': 'minotaure',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Corne de taureau en or',
                    },
                    {
                        'id': 'l2r3_nike',
                        'x': 1050, 'y': 160, 'largeur': 70, 'hauteur': 120,
                        'label': 'Victoire ailee',
                        'indice': (
                            "Cette celebre statue representant une victoire ailee\n"
                            "vient de l ile de Samothrace.\n"
                            "Elle represente quelle deesse ?"
                        ),
                        'reponse': 'nike',
                        'digit_index': 1, 'digit_value': 4,
                        'bijou': 'Aile d\'or de Nike',
                    },
                ],
            },
            4: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l2r4_socrate',
                        'x': 550, 'y': 200, 'largeur': 80, 'hauteur': 100,
                        'label': 'Buste philosophe',
                        'indice': (
                            "Ce buste represente un grand philosophe grec.\n"
                            "Il disait « Je sais que je ne sais rien ».\n"
                            "Son nom ?"
                        ),
                        'reponse': 'socrate',
                        'digit_index': 2, 'digit_value': 9,
                        'bijou': 'Bague de sagesse en or',
                    },
                    {
                        'id': 'l2r4_acropole',
                        'x': 1100, 'y': 180, 'largeur': 90, 'hauteur': 80,
                        'label': 'Maquette d Acropole',
                        'indice': (
                            "Ce temple au sommet de l Acropole est dedié\n"
                            "a la deesse de la sagesse.\n"
                            "Comment s appelle ce temple ?"
                        ),
                        'reponse': 'parthenon',
                        'digit_index': 3, 'digit_value': 1,
                        'bijou': 'Drachme antique en argent',
                    },
                ],
            },
            5: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l2r5_ulysse',
                        'x': 400, 'y': 190, 'largeur': 80, 'hauteur': 110,
                        'label': 'Carte d Ulysse',
                        'indice': (
                            "Cette carte represente le voyage du heros.\n"
                            "Il mit 10 ans pour rentrer chez lui apres\n"
                            "la guerre de Troie. Comment s appelait-il ?"
                        ),
                        'reponse': 'ulysse',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Rubis d\'Ithaque',
                    },
                    {
                        'id': 'l2r5_hermes',
                        'x': 1050, 'y': 170, 'largeur': 70, 'hauteur': 120,
                        'label': 'Sandales ailees',
                        'indice': (
                            "Ces sandales ailees appartiennent au messager\n"
                            "des dieux et dieu du commerce.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'hermes',
                        'digit_index': 1, 'digit_value': 0,
                        'bijou': 'Sandale d\'or d\'Hermes',
                    },
                ],
            },
        },
    },

    3: {
        'name': 'Renaissance Italienne',
        'rooms': {
            1: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r1_mona',
                        'x': 400, 'y': 200, 'largeur': 80, 'hauteur': 100,
                        'label': 'Tableau au sourire',
                        'indice': (
                            "Un tableau celebre represente une femme\n"
                            "avec un sourire mysterieux.\n"
                            "Quel est son prenom en 4 lettres ?"
                        ),
                        'reponse': 'mona',
                        'digit_index': 0, 'digit_value': 4,
                        'bijou': 'Perle baroque de la Joconde',
                    },
                    {
                        'id': 'l3r1_leonard',
                        'x': 950, 'y': 180, 'largeur': 80, 'hauteur': 100,
                        'label': 'Carnet de croquis',
                        'indice': (
                            "Ce carnet appartient au peintre de la Joconde.\n"
                            "Il etait aussi sculpteur, ingenieur et inventeur.\n"
                            "Son prenom ?"
                        ),
                        'reponse': 'leonard',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Loupe de Leonard en cristal',
                    },
                ],
            },
            2: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r2_raphael',
                        'x': 550, 'y': 170, 'largeur': 80, 'hauteur': 110,
                        'label': 'Grande peinture',
                        'indice': (
                            "Ce peintre de la Renaissance a represente\n"
                            "de nombreuses Vierges a l Enfant.\n"
                            "Son prenom ?"
                        ),
                        'reponse': 'raphael',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Medaillon de la Vierge en or',
                    },
                    {
                        'id': 'l3r2_coupole',
                        'x': 1100, 'y': 190, 'largeur': 70, 'hauteur': 90,
                        'label': 'Plan de cathedrale',
                        'indice': (
                            "Cet architecte a concu la coupole du Dome\n"
                            "de Florence. Il a invente la perspective lineaire.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'brunelleschi',
                        'digit_index': 3, 'digit_value': 9,
                        'bijou': 'Pierre de Florence en marbre rose',
                    },
                ],
            },
            3: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r3_botticelli',
                        'x': 450, 'y': 190, 'largeur': 90, 'hauteur': 100,
                        'label': 'Naissance d une deesse',
                        'indice': (
                            "Ce tableau montre une deesse emergent de la mer\n"
                            "sur une coquille. Son auteur est Botticelli.\n"
                            "Quelle deesse est representee ?"
                        ),
                        'reponse': 'venus',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Coquille en nacre de Venus',
                    },
                    {
                        'id': 'l3r3_mecene',
                        'x': 1000, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Blason de famille',
                        'indice': (
                            "Cette famille florentine financa de nombreux\n"
                            "artistes de la Renaissance, dont Leonard.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'medicis',
                        'digit_index': 1, 'digit_value': 3,
                        'bijou': 'Emeraude des Medicis',
                    },
                ],
            },
            4: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r4_michel',
                        'x': 600, 'y': 160, 'largeur': 70, 'hauteur': 120,
                        'label': 'Esquisse de statue',
                        'indice': (
                            "Cet artiste a sculpte le David et peint\n"
                            "la chapelle Sixtine.\n"
                            "Son prenom ?"
                        ),
                        'reponse': 'michel-ange',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Bloc de marbre de Carrare',
                    },
                    {
                        'id': 'l3r4_fresque',
                        'x': 1100, 'y': 180, 'largeur': 80, 'hauteur': 100,
                        'label': 'Fragment de fresque',
                        'indice': (
                            "Cette fresque ornait un plafond de palais.\n"
                            "La technique consiste a peindre sur du platre frais.\n"
                            "Comment appelle-t-on cette technique ?"
                        ),
                        'reponse': 'fresque',
                        'digit_index': 3, 'digit_value': 1,
                        'bijou': 'Pigment de lapis-lazuli Renaissance',
                    },
                ],
            },
            5: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r5_titian',
                        'x': 400, 'y': 180, 'largeur': 80, 'hauteur': 110,
                        'label': 'Portrait royal',
                        'indice': (
                            "Ce peintre venitien etait celebre pour\n"
                            "ses portraits et ses couleurs chaudes.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'titien',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Rubis de Venise',
                    },
                    {
                        'id': 'l3r5_sfumato',
                        'x': 1000, 'y': 190, 'largeur': 90, 'hauteur': 90,
                        'label': 'Detail de tableau',
                        'indice': (
                            "Leonard de Vinci inventa cette technique\n"
                            "qui estompe les contours dans un voile de fumee.\n"
                            "Comment s appelle cette technique ?"
                        ),
                        'reponse': 'sfumato',
                        'digit_index': 1, 'digit_value': 0,
                        'bijou': 'Diamant taille en sfumato',
                    },
                ],
            },
        },
    },

    4: {
        'name': 'France Royale',
        'rooms': {
            1: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l4r1_louvre_annee',
                        'x': 500, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Plaque commemorative',
                        'indice': (
                            "Une plaque sur le mur indique :\n"
                            "« Je suis ne en cette annee, je suis le plus\n"
                            "grand musee de France. »\n"
                            "Quelle est cette annee ?"
                        ),
                        'reponse': '1793',
                        'digit_index': 0, 'digit_value': 4,
                        'bijou': 'Clef du Louvre en or',
                    },
                    {
                        'id': 'l4r1_napoleon',
                        'x': 1050, 'y': 170, 'largeur': 80, 'hauteur': 110,
                        'label': 'Portrait imperial',
                        'indice': (
                            "Cet empereur a grandement enrichi\n"
                            "les collections du Louvre.\n"
                            "Son prenom ?"
                        ),
                        'reponse': 'napoleon',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Medaille imperiale en bronze',
                    },
                ],
            },
            2: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l4r2_drapeau',
                        'x': 450, 'y': 190, 'largeur': 90, 'hauteur': 80,
                        'label': 'Drapeau tricolore',
                        'indice': (
                            "Remettez les couleurs dans l ordre\n"
                            "du drapeau francais (separees par des tirets) :"
                        ),
                        'reponse': 'bleu-blanc-rouge',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Cocarde tricolore en rubis et saphir',
                    },
                    {
                        'id': 'l4r2_versailles',
                        'x': 1000, 'y': 200, 'largeur': 80, 'hauteur': 100,
                        'label': 'Maquette de chateau',
                        'indice': (
                            "Ce chateau fut la residence principale\n"
                            "de Louis XIV, le Roi Soleil.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'versailles',
                        'digit_index': 3, 'digit_value': 9,
                        'bijou': 'Lustre en cristal de Versailles',
                    },
                ],
            },
            3: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l4r3_couronne',
                        'x': 550, 'y': 170, 'largeur': 80, 'hauteur': 100,
                        'label': 'Vitrine de la couronne',
                        'indice': (
                            "Ce joyau est place au sommet de la couronne royale.\n"
                            "Il symbolise la puissance divine du roi.\n"
                            "Comment s appelle la plus grande pierre de la couronne ?"
                        ),
                        'reponse': 'regent',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Le diamant Regent (replique)',
                    },
                    {
                        'id': 'l4r3_sceptre',
                        'x': 1100, 'y': 180, 'largeur': 60, 'hauteur': 120,
                        'label': 'Sceptre royal',
                        'indice': (
                            "Ce sceptre royal etait utilise lors des\n"
                            "sacres des rois de France.\n"
                            "Combien de fleurs de lys orne-t-il ? (reponse : 3)"
                        ),
                        'reponse': '3',
                        'digit_index': 1, 'digit_value': 3,
                        'bijou': 'Sceptre miniature en or',
                    },
                ],
            },
            4: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l4r4_jeanne',
                        'x': 400, 'y': 190, 'largeur': 80, 'hauteur': 110,
                        'label': 'Armure medievale',
                        'indice': (
                            "Cette jeune femme portait armure et delivra\n"
                            "Orleans en 1429 avant d etre brulee.\n"
                            "Son prenom ?"
                        ),
                        'reponse': 'jeanne',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Etendard de Jeanne en soie brodee d\'or',
                    },
                    {
                        'id': 'l4r4_lutetia',
                        'x': 1000, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Carte ancienne',
                        'indice': (
                            "Cette carte montre l ancien nom romain de Paris.\n"
                            "Comment s appelait Paris a l epoque romaine ?"
                        ),
                        'reponse': 'lutetia',
                        'digit_index': 3, 'digit_value': 1,
                        'bijou': 'Monnaie gauloise en electrum',
                    },
                ],
            },
            5: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l4r5_louvre_lettres',
                        'x': 500, 'y': 190, 'largeur': 80, 'hauteur': 100,
                        'label': 'Panneau de securite',
                        'indice': (
                            "Code de securite :\n"
                            "Combien de lettres dans le mot LOUVRE ?"
                        ),
                        'reponse': '6',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Emeraude imperiale de Napoleon',
                    },
                    {
                        'id': 'l4r5_pyramide_louvre',
                        'x': 1050, 'y': 180, 'largeur': 90, 'hauteur': 100,
                        'label': 'Maquette de pyramide',
                        'indice': (
                            "Cette pyramide en verre se trouve dans\n"
                            "la cour du Louvre depuis 1989.\n"
                            "En quelle matiere est-elle construite ?"
                        ),
                        'reponse': 'verre',
                        'digit_index': 1, 'digit_value': 0,
                        'bijou': 'Prisme de verre de la Pyramide',
                    },
                ],
            },
        },
    },

    5: {
        'name': 'La Grande Finale',
        'rooms': {
            1: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r1_couloir',
                        'x': 400, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Tableau numerote',
                        'indice': (
                            "Derriere ce tableau se cache un code.\n"
                            "L annee de fondation du Louvre en ordre inverse ?\n"
                            "(ex : 1793 a l envers)"
                        ),
                        'reponse': '3971',
                        'digit_index': 0, 'digit_value': 4,
                        'bijou': 'Cle secrete en titane',
                    },
                    {
                        'id': 'l5r1_gardien',
                        'x': 1000, 'y': 180, 'largeur': 80, 'hauteur': 100,
                        'label': 'Uniforme de gardien',
                        'indice': (
                            "Combien de tableaux le Louvre possede-t-il\n"
                            "approximativement ? (reponse attendue : 35000)"
                        ),
                        'reponse': '35000',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Badge du gardien en or',
                    },
                ],
            },
            2: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r2_archives',
                        'x': 500, 'y': 190, 'largeur': 80, 'hauteur': 100,
                        'label': 'Dossier secret',
                        'indice': (
                            "Le mot est anagramme : VREOLU.\n"
                            "Remettez les lettres dans l ordre."
                        ),
                        'reponse': 'louvre',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Cachet secret du Louvre',
                    },
                    {
                        'id': 'l5r2_coffre',
                        'x': 1050, 'y': 170, 'largeur': 90, 'hauteur': 100,
                        'label': 'Coffre-fort',
                        'indice': (
                            "Le code du coffre est la somme\n"
                            "des chiffres de l annee de fondation du Louvre.\n"
                            "1+7+9+3 = ?"
                        ),
                        'reponse': '20',
                        'digit_index': 3, 'digit_value': 9,
                        'bijou': 'Lingot d\'or du tresor',
                    },
                ],
            },
            3: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r3_laser',
                        'x': 450, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Panneau de controle',
                        'indice': (
                            "Pour desactiver les lasers, entrez\n"
                            "le nombre de salles du musee du Louvre.\n"
                            "Il y en a environ 403."
                        ),
                        'reponse': '403',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Carte electronique du systeme',
                    },
                    {
                        'id': 'l5r3_equation',
                        'x': 1050, 'y': 180, 'largeur': 70, 'hauteur': 100,
                        'label': 'Tableau d equations',
                        'indice': (
                            "Resolvez : 4x + 12 = 0\n"
                            "Que vaut x ?"
                        ),
                        'reponse': '-3',
                        'digit_index': 1, 'digit_value': 3,
                        'bijou': 'Cube en diamant mathematique',
                    },
                ],
            },
            4: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r4_victoire_sam',
                        'x': 550, 'y': 160, 'largeur': 70, 'hauteur': 130,
                        'label': 'Socle vide',
                        'indice': (
                            "Cette statue ailee sans tete ni bras vient\n"
                            "d une ile grecque. Elle est au Louvre depuis 1884.\n"
                            "De quelle ile vient-elle ?"
                        ),
                        'reponse': 'samothrace',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Fragment d\'aile en marbre blanc',
                    },
                    {
                        'id': 'l5r4_hamourabi',
                        'x': 1100, 'y': 170, 'largeur': 60, 'hauteur': 120,
                        'label': 'Stele de lois',
                        'indice': (
                            "Cette stele contient le plus ancien\n"
                            "code de lois connu de l humanite.\n"
                            "Le nom du roi qui l a commande ?"
                        ),
                        'reponse': 'hammourabi',
                        'digit_index': 3, 'digit_value': 1,
                        'bijou': 'Tablette d\'argile en or',
                    },
                ],
            },
            5: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r5_final_mona',
                        'x': 600, 'y': 150, 'largeur': 80, 'hauteur': 130,
                        'label': 'LA Joconde',
                        'indice': (
                            "Face au tableau le plus visite du monde.\n"
                            "Le peintre est Leonardo da Vinci.\n"
                            "En quelle annee a-t-il peint la Joconde ?"
                            "\n(entre 1503 et 1519, reponse : 1503)"
                        ),
                        'reponse': '1503',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'LE GRAND BUTIN : Couronne de la Joconde',
                    },
                    {
                        'id': 'l5r5_final_pyramide',
                        'x': 1050, 'y': 180, 'largeur': 90, 'hauteur': 100,
                        'label': 'Coeur de la Pyramide',
                        'indice': (
                            "La pyramide du Louvre a ete inauguree\n"
                            "sous quel president de la Republique ?\n"
                            "(son nom de famille)"
                        ),
                        'reponse': 'mitterrand',
                        'digit_index': 1, 'digit_value': 0,
                        'bijou': 'Diamant de la Pyramide du Louvre',
                    },
                ],
            },
        },
    },
}


def get_room(level_id, room_id):
    import copy
    lvl = LEVELS.get(level_id, {})
    room = lvl.get('rooms', {}).get(room_id)
    if room is None:
        return None
    r = copy.deepcopy(room)
    for e in r['enigmes']:
        e.setdefault('resolu', False)
    r.setdefault('porte_resolue', False)

    enigmes = r['enigmes']
    n = len(enigmes)
    digits = ['0'] * 4
    if n == 1:
        dv = enigmes[0]['digit_value']
        digits = [str(dv)] * 4
    elif n == 2:
        d0, i0 = enigmes[0]['digit_value'], enigmes[0]['digit_index']
        d1, i1 = enigmes[1]['digit_value'], enigmes[1]['digit_index']
        digits[0] = str(d0)
        digits[1] = str((d0 + i0 + 1) % 10)
        digits[2] = str(d1)
        digits[3] = str((d1 + i1 + 1) % 10)
    else:
        for i, e in enumerate(enigmes[:4]):
            digits[i] = str(e['digit_value'])
    r['code_porte'] = ''.join(digits)
    return r


def get_nb_rooms(level_id):
    return len(LEVELS.get(level_id, {}).get('rooms', {}))

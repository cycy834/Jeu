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
                        'label': 'Stèle aux hiéroglyphes',
                        'indice': (
                            "Une stèle couverte de symboles égyptiens.\n"
                            "Le cartouche du bas désigne la pierre qui permit\n"
                            "de déchiffrer les hiéroglyphes. Son nom ?"
                        ),
                        'reponse': 'rosette',
                        'digit_index': 0, 'digit_value': 4,
                        'bijou': 'Scarabée en or',
                    },
                    {
                        'id': 'l1r1_nil',
                        'x': 1190, 'y': 206, 'largeur': 90, 'hauteur': 130,
                        'label': 'Carte ancienne',
                        'indice': (
                            "Ce fleuve traversait l\'Egypte et permettait\n"
                            "aux terres de rester fertiles.\n"
                            "Son nom en 3 lettres ?"
                        ),
                        'reponse': 'nil',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Perle bleue du Nil',
                    },
                ],
            },
            2: {
                'bg': 7,
                'depart': (80, 300),
                'porte': (760, 158),
                'enigmes': [
                    {
                        'id': 'l1r2_cleopatre',
                        'x': 270, 'y': 150, 'largeur': 90, 'hauteur': 200,
                        'label': 'Portrait royal',
                        'indice': (
                            "Cette reine égyptienne est célèbre pour.\n"
                            "son histoire avec Jules César.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'cleopatre',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Couronne d\'émeraudes',
                    },
                    {
                        'id': 'l1r2_momie',
                        'x': 1150, 'y': 150, 'largeur': 90, 'hauteur': 200,
                        'label': 'Tombe ancienne',
                        'indice': (
                            "Les Egyptiens enveloppaient les corps\n"
                            "dans des bandes pour les conserver.\n"
                            "Comment appelle-t-on cela ?"
                        ),
                        'reponse': 'momie',
                        'digit_index': 3, 'digit_value': 9,
                        'bijou': 'Bracelet du pharaon',
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
                            "Les Egyptiens utilisaient cette plante.\n"
                            "pour fabriquer un support d\'écriture.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'papyrus',
                        'digit_index': 0, 'digit_value': 3,
                        'bijou': 'Rouleau doré',
                    },
                    {
                        'id': 'l1r3_sphinx',
                        'x': 1130, 'y': 163, 'largeur': 90, 'hauteur': 200,
                        'label': 'Sphinx miniature',
                        'indice': (
                            "Créature mi-homme mi-lion gardienne des pyramides.\n"
                            "Le plus célèbre se trouve a Gizeh.\n"
                            "Comment appelle-t-on cette créature ?"
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
                        'id': 'l1r4_chat',
                        'x': 370, 'y': 188, 'largeur': 90, 'hauteur': 120,
                        'label': 'Statue de chat',
                        'indice': (
                            "Cet animal était sacré en Egypte.\n"
                            "Il était lié à la déesse astet.\n"
                            "Quel est cet animal ?"
                        ),
                        'reponse': 'chat',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Chat en or massif',
                    },
                    {
                        'id': 'l1r4_canope',
                        'x': 1050, 'y': 180, 'largeur': 100, 'hauteur': 130,
                        'label': 'Vase canope',
                        'indice': (
                            "Ces vases conservaient les organes des défunts embaumes.\n"
                            "Il y en avait toujours un nombre précis par momie.\n"
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
                        'id': 'l1r5_osiris',
                        'x': 210, 'y': 146, 'largeur': 110, 'hauteur': 200,
                        'label': 'Sanctuaire d\'Osiris',
                        'indice': (
                            "Ce dieu égyptien est associé au monde des morts.\n"
                            "et son épouse est Isis.\n"
                            "Comment s appelle-t-it ?"
                        ),
                        'reponse': 'Osiris',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Amulette d\'Osiris',
                    },
                    {
                        'id': 'l1r5_scarabee',
                        'x': 680, 'y': 155, 'largeur': 120, 'hauteur': 160,
                        'label': 'Amulette gravée',
                        'indice': (
                            "Cet insecte était un symbole de renaissance.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'scarabee',
                        'digit_index': 1, 'digit_value': 0,
                        'bijou': 'Scarabée doré',
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
                        'id': 'l2r1_aphrodite',
                        'x': 700, 'y': 150, 'largeur': 60, 'hauteur': 130,
                        'label': 'Statue sans bras',
                        'indice': (
                            "Cette statue de femme sans bras est l\'une\n"
                            "des sculptures les plus célèbres du Louvre.\n"
                            "Elle représente la déesse grecque de l\'amour. Son nom ?"
                        ),
                        'reponse': 'aphrodite',
                        'digit_index': 0, 'digit_value': 5,
                        'bijou': 'Collier de perles d Aphrodite',
                    },
                    {
                        'id': 'l2r1_poseidon',
                        'x': 1100, 'y': 170, 'largeur': 80, 'hauteur': 110,
                        'label': 'Trident',
                        'indice': (
                            "Ce trident appartient au dieu des mers.\n"
                            "Frère de Zeus et d\'Hadès.\n"
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
                        'id': 'l2r2_troie',
                        'x': 500, 'y': 200, 'largeur': 70, 'hauteur': 110,
                        'label': 'Guerre célèbre',
                        'indice': (
                            "Cette amphore représente des guerriers.\n"
                            "La scène montre le fameux cheval de bois\n"
                            "utilisé pour entrer dans une cité. Laquelle ?"
                        ),
                        'reponse': 'troie',
                        'digit_index': 2, 'digit_value': 7,
                        'bijou': 'Fibule en bronze de Troie',
                    },
                    {
                        'id': 'l2r2_meduse',
                        'x': 1000, 'y': 190, 'largeur': 80, 'hauteur': 90,
                        'label': 'Statue pétrifiée',
                        'indice': (
                            "Son regard dangereux pouvait pétrifier quiconque le croisait\n"
                            "et ses cheveux bougeaient ?\n"
                            "Son nom ?"
                        ),
                        'reponse': 'meduse',
                        'digit_index': 3, 'digit_value': 2,
                        'bijou': 'Serpent d\'or',
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
                            "Ce plan représente le labyrinthe de Crète.\n"
                            "Il enfermait une créature mi-homme mi-taureau.\n"
                            "Comment s\'appelait ce monstre ?"
                        ),
                        'reponse': 'minotaure',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Corne de taureau en or',
                    },
                    {
                        'id': 'l2r3_pegase',
                        'x': 1050, 'y': 160, 'largeur': 70, 'hauteur': 120,
                        'label': 'Cheval de marbre',
                        'indice': (
                            "Créature blanche légendaire capable de voler.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'pegase',
                        'digit_index': 1, 'digit_value': 4,
                        'bijou': 'Plume d\'argent',
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
                            "Ce buste représente un grand philosophe grec.\n"
                            "Il disait « Je sais que je ne sais rien ».\n"
                            "Son nom ?"
                        ),
                        'reponse': 'socrate',
                        'digit_index': 2, 'digit_value': 9,
                        'bijou': 'Bague de sagesse en or',
                    },
                    {
                        'id': 'l2r4_cyclope',
                        'x': 1100, 'y': 180, 'largeur': 90, 'hauteur': 80,
                        'label': 'Créature mythologique',
                        'indice': (
                            "Cette créature possède une particularité :\n"
                            "elle n'a qu'un seul oeil.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'cyclope',
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
                            "Cette carte représente le voyage d\'un héros.\n"
                            "Il mit 10 ans pour rentrer chez lui après\n"
                            "la guerre de Troie. Comment s\'appelait-il ?"
                        ),
                        'reponse': 'ulysse',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Rubis d\'Ithaque',
                    },
                    {
                        'id': 'l2r5_hermes',
                        'x': 1050, 'y': 170, 'largeur': 70, 'hauteur': 120,
                        'label': 'Sandales ailées',
                        'indice': (
                            "Ces sandales ailées appartiennent au messager\n"
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
                            "Un tableau célèbre représente une femme\n"
                            "avec un sourire mystérieux.\n"
                            "Quel est son prénom en 4 lettres ?"
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
                            "Il était aussi sculpteur, ingénieur et inventeur.\n"
                            "Son prénom ?"
                        ),
                        'reponse': 'leonard',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Loupe de Léonard en cristal',
                    },
                ],
            },
            2: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r2_sixtine',
                        'x': 550, 'y': 170, 'largeur': 80, 'hauteur': 110,
                        'label': 'Plafond peint',
                        'indice': (
                            "Cette célèbre chapelle est connue\n"
                            "pour son immense plafond peint.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'sixtine',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Fragment de fresque',
                    },
                    {
                        'id': 'l3r2_italie',
                        'x': 1100, 'y': 190, 'largeur': 70, 'hauteur': 90,
                        'label': 'Globe ancien',
                        'indice': (
                            "Pays où est née la Renaissance.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'italie',
                        'digit_index': 3, 'digit_value': 9,
                        'bijou': 'Saphir italien',
                    },
                ],
            },
            3: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r3_venus',
                        'x': 450, 'y': 190, 'largeur': 90, 'hauteur': 100,
                        'label': 'Naissance d\'une déesse',
                        'indice': (
                            "Ce tableau montre une déesse émergent de la mer\n"
                            "sur une coquille. Son auteur est Botticelli.\n"
                            "Quelle déesse est représentée ?"
                        ),
                        'reponse': 'venus',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Coquille en nacre de Vénus',
                    },
                    {
                        'id': 'l3r3_portrait',
                        'x': 1000, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Toile mystérieuse',
                        'indice': (
                            "Nom donné à une oeuvre représentant une personne.\n"
                            "Ce mot ?"
                        ),
                        'reponse': 'portrait',
                        'digit_index': 1, 'digit_value': 3,
                        'bijou': 'Cadre de cristal',
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
                            "Cet artiste a sculpté le David et peint\n"
                            "la chapelle Sixtine.\n"
                            "Son prénom ?"
                        ),
                        'reponse': 'michel-ange',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Fresque de Michel-Ange',
                    },
                    {
                        'id': 'l3r4_pise',
                        'x': 1100, 'y': 180, 'largeur': 80, 'hauteur': 100,
                        'label': 'Maquette célèbre',
                        'indice': (
                            "Cette ville italienne est connue pour\n"
                            "une tour qui penche.\n"
                            "Comment appelle-t-on cette tour ?"
                        ),
                        'reponse': 'pise',
                        'digit_index': 3, 'digit_value': 1,
                        'bijou': 'Tour miniature',
                    },
                ],
            },
            5: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l3r5_colomb',
                        'x': 400, 'y': 180, 'largeur': 80, 'hauteur': 110,
                        'label': 'Carte maritime',
                        'indice': (
                            "Cet explorateur traversa  l\'Atlantique\n"
                            "et atteignit l\'Amérique en 1492.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'colomb',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Boussole dorée',
                    },
                    {
                        'id': 'l3r5_vatican',
                        'x': 1000, 'y': 190, 'largeur': 90, 'hauteur': 90,
                        'label': 'Muraille miniature',
                        'indice': (
                            "Ce minuscule Etat se trouve au coeur de Rome.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'vatican',
                        'digit_index': 1, 'digit_value': 0,
                        'bijou': 'Emeraude florentine',
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
                        'label': 'Plaque commémorative',
                        'indice': (
                            "Une plaque sur le mur indique :\n"
                            "« Je suis né en cette annee, je suis le plus\n"
                            "grand musée de France. »\n"
                            "Quelle est cette année ?"
                        ),
                        'reponse': '1793',
                        'digit_index': 0, 'digit_value': 4,
                        'bijou': 'Clef du Louvre en or',
                    },
                    {
                        'id': 'l4r1_napoleon',
                        'x': 1050, 'y': 170, 'largeur': 80, 'hauteur': 110,
                        'label': 'Portrait impérial',
                        'indice': (
                            "Cet empereur se fit sacrer en 1804 et a grandement\n"
                            "enrichi les collections du Louvre.\n"
                            "Son prénom ?"
                        ),
                        'reponse': 'napoleon',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Medaille impériale en bronze',
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
                            "Remettez les couleurs dans l\'ordre\n"
                            "du drapeau français (séparées par des tirets) :"
                        ),
                        'reponse': 'bleu-blanc-rouge',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Cocarde tricolore en rubis et saphir',
                    },
                    {
                        'id': 'l4r2_versailles',
                        'x': 1000, 'y': 200, 'largeur': 80, 'hauteur': 100,
                        'label': 'Maquette de château',
                        'indice': (
                            "Ce château fut la résidence principale\n"
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
                        'id': 'l4r3_bastille',
                        'x': 550, 'y': 170, 'largeur': 80, 'hauteur': 100,
                        'label': 'Forteresse impériale',
                        'indice': (
                            "Cette prison parisienne fut prise au\n"
                            "début de la Révolution française.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'bastille',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Le diamant Regent (replique)',
                    },
                    {
                        'id': 'l4r3_lys',
                        'x': 1100, 'y': 180, 'largeur': 60, 'hauteur': 120,
                        'label': 'Bannière royale',
                        'indice': (
                            "Ce symbole était associé à la monarchie\n"
                            "française et est aussi une fleur.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'lys',
                        'digit_index': 1, 'digit_value': 3,
                        'bijou': 'Fleur royale en or',
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
                        'label': 'Armure médiévale',
                        'indice': (
                            "Cette jeune femme portait une armure et délivra\n"
                            "Orleans en 1429 avant d\'être brulée.\n"
                            "Son prénom ?"
                        ),
                        'reponse': 'jeanne',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Etendard de Jeanne en soie brodée d\'or',
                    },
                    {
                        'id': 'l4r4_tuileries',
                        'x': 1000, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Palais disparu',
                        'indice': (
                            "Cet ancien palais parisien se trouvait près du Louvre.\n"
                            "C'est aussi aujourdh\'hui le nom d'un parc parisien célèbre.\n"
                            "Quel est son nom ?"
                        ),
                        'reponse': 'tuileries',
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
                        'label': 'Panneau de sécurite',
                        'indice': (
                            "Code de sécurite :\n"
                            "Combien de lettres dans le mot LOUVRE ?"
                        ),
                        'reponse': '6',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'Collier en diamands',
                    },
                    {
                        'id': 'l4r5_pyramide_louvre',
                        'x': 1050, 'y': 180, 'largeur': 90, 'hauteur': 100,
                        'label': 'Maquette de pyramide',
                        'indice': (
                            "Cette pyramide en verre se trouve dans\n"
                            "la cour du Louvre depuis 1989.\n"
                            "En quelle matière est-elle construite ?"
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
                        'label': 'Portrait lumineux',
                        'indice': (
                            "Quel numéro portait le Roi Soleil ?\n"
                        ),
                        'reponse': '14',
                        'digit_index': 0, 'digit_value': 4,
                        'bijou': 'Sceptre solaire',
                    },
                    {
                        'id': 'l5r1_arc',
                        'x': 1000, 'y': 180, 'largeur': 80, 'hauteur': 100,
                        'label': 'Monument parisien',
                        'indice': (
                            "Completez le monument parisien suivant :\n"
                            "Arc de ____"
                        ),
                        'reponse': 'triomphe',
                        'digit_index': 1, 'digit_value': 7,
                        'bijou': 'Arche en or',
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
                            "Le mot est un anagramme : VREOLU.\n"
                            "Remettez les lettres dans l\'ordre."
                        ),
                        'reponse': 'voleur',
                        'digit_index': 2, 'digit_value': 2,
                        'bijou': 'Cachet secret du Louvre',
                    },
                    {
                        'id': 'l5r2_coffre',
                        'x': 1050, 'y': 170, 'largeur': 90, 'hauteur': 100,
                        'label': 'Coffre-fort',
                        'indice': (
                            "Le code du coffre est la somme\n"
                            "des chiffres de l\'année de fondation du Louvre.\n"
                            "1+7+9+3 = ____ ?"
                        ),
                        'reponse': '20',
                        'digit_index': 3, 'digit_value': 9,
                        'bijou': 'Lingot d\'or du trésor',
                    },
                ],
            },
            3: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r3_hymne',
                        'x': 450, 'y': 200, 'largeur': 80, 'hauteur': 90,
                        'label': 'Partition ancienne',
                        'indice': (
                            "Quel est le nom de l\'hymne national français ?"
                        ),
                        'reponse': 'marseillaise',
                        'digit_index': 0, 'digit_value': 6,
                        'bijou': 'Partition royale',
                    },
                    {
                        'id': 'l5r3_equation',
                        'x': 1050, 'y': 180, 'largeur': 70, 'hauteur': 100,
                        'label': 'Tableau d\'équations',
                        'indice': (
                            "Résolvez : 4x + 12 = 0\n"
                            "Que vaut x ?"
                        ),
                        'reponse': '-3',
                        'digit_index': 1, 'digit_value': 3,
                        'bijou': 'Cube en diamant mathématique',
                    },
                ],
            },
            4: {
                'bg': 2,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r4_monnaie',
                        'x': 550, 'y': 160, 'largeur': 70, 'hauteur': 130,
                        'label': 'Pièce royale',
                        'indice': (
                            "Avant l\'euro, quelle monnaie était\n"
                            "utilisée en France ?\n"
                        ),
                        'reponse': 'franc',
                        'digit_index': 2, 'digit_value': 5,
                        'bijou': 'Pièce du royaume',
                    },
                    {
                        'id': 'l5r4_concorde',
                        'x': 1100, 'y': 170, 'largeur': 60, 'hauteur': 120,
                        'label': 'Place royale',
                        'indice': (
                            "Cette grande place parisienne acueille\n"
                            "l'obélisque égyptien.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'concorde',
                        'digit_index': 3, 'digit_value': 1,
                        'bijou': 'Clé de la Concorde',
                    },
                ],
            },
            5: {
                'bg': 1,
                'depart': (100, 300),
                'porte': (1460, 180),
                'enigmes': [
                    {
                        'id': 'l5r5_tour',
                        'x': 600, 'y': 150, 'largeur': 80, 'hauteur': 130,
                        'label': 'Maquette métallique',
                        'indice': (
                            "Monument parisien construit pour\n"
                            "l\'Exposition universelle de 1889.\n"
                            "La Tour ____ ?"
                        ),
                        'reponse': 'eiffel',
                        'digit_index': 0, 'digit_value': 8,
                        'bijou': 'LE GRAND BUTIN : Couronne de la Joconde',
                    },
                    {
                        'id': 'l5r5_titanic',
                        'x': 1050, 'y': 180, 'largeur': 90, 'hauteur': 100,
                        'label': 'Crosière ancienne',
                        'indice': (
                            "Paquebot célèbre ayant coulé en 1912.\n"
                            "Son nom ?"
                        ),
                        'reponse': 'titanic',
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

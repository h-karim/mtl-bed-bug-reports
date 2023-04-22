class Parser:
    pass


class Entry:
    """point: (X,Y)
    date: (yyyy/mm/dd) use date_declaration
    """
    pass


"""Déclarations

NO_DECLARATION : Numéro unique de déclaration
DATE_DECLARATION : Date de la déclaration
DATE_INSP_VISPRE : Date d'inspection préalable
NBR_EXTERMIN : Dans le cadre de l'intervention déclarée, nombre de fois qu'une extermination a été effectuée. Chaque extermination peut viser un ou plusieurs logements. De multiples exterminations notées pour une déclaration indiquent que le gestionnaire de parasite a constaté des indices de punaises de lit suite à l'extermination précédente et qu'il a réalisé une nouvelle extermination. Le nombre maximal d'exterminations permis par déclaration est de 4.
DATE_DEBUTTRAIT : Date de début de la première extermination associée à la déclaration
DATE_FINTRAIT : Date de fin de la dernière extermination associée à la déclaration
No_QR : Numéro du quartier de référence
NOM_QR : Nom du quartier de référence
NOM_ARROND : Nom de l'arrondissement
COORD_X :Coordonnées X (NAD83 MTM8)
COORD_Y : Coordonnées Y (NAD83 MTM8)
LONGITUDE : Coordonnées (WGS84)
LATITUDE: Coordonnées (WGS84)

"""

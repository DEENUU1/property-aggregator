from enum import Enum


class BuildingTypeEnum(str, Enum):
    APARTAMENTOWIEC = "Apartamentowiec"
    BLOK = "Blok"
    KAMIENICA = "Kamienica"
    POZOSTALE = "Pozostałe"
    LOFT = "Loft"

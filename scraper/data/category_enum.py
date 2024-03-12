from enum import Enum


class CategoryEnum(str, Enum):
    MIESZKANIE = "Mieszkanie"
    POKOJ = "Pokój"
    DOM = "Dom"
    DZIALKA = "DZIAŁKA"
    BIURA_I_LOKALE = "Biura i lokale"
    GARAZE_I_PARKINGI = "Garaże i parkingi"
    STANCJE_I_POKOJE = "Stancje i pokoje"
    HALE_I_MAGAZYNY = "Hale i magazyny"
    POZOSTALE = "Pozostałe"

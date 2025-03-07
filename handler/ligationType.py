from enum import Enum

class LigationType(Enum):
    COVALENTE_DATIVA_MEDIA = 'd2'
    COVALENTE_DATIVA = 'd'
    COVALENTE = 'c'
    IONICA = 'i'
    LIGACAO_DE_HIDROGENIO = 'h'

    def match_ligation_type(text:str):
        return LigationType(text)
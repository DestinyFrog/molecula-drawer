from enum import Enum

class LigationType(Enum):
    COVALENTE_DATIVA = 'd'
    COVALENTE = 'c'
    IONICA = 'i'
    LIGACAO_DE_HIDROGENIO = 'h'

    def match_ligation_type(text:str):
        match text:
            case 'd':
                return LigationType.COVALENTE_DATIVA
            case 'c':
                return LigationType.COVALENTE
            case 'i':
                return LigationType.IONICA
            case 'h':
                return LigationType.LIGACAO_DE_HIDROGENIO
        return None
from handler.sectionHandler import SectionHandler
from handler.types import LigationType

class Handler(SectionHandler):
    def __init__(self, content:str):
        super(Handler, self).__init__(content)

    def match_eletrons(self, text:str):
        match text:
            case '%':
                return 3
            case '=':
                return 2
            case '-':
                return 1
        return None

    def match_patterns(self, text:str) -> list[float]:
        match text:
            case 'benz' | 'benZ':
                return [
                    (30, 2, LigationType.COVALENTE, []),
                    (90, 1, LigationType.COVALENTE, []),
                    (150, 2, LigationType.COVALENTE, []),
                    (210, 1, LigationType.COVALENTE, []),
                    (270, 2, LigationType.COVALENTE, []),
                    (150, 1, LigationType.COVALENTE, [])
                ]

            case 'hexagonal' | 'hexA':
                return [
                    (30, 1, LigationType.COVALENTE, []),
                    (90, 1, LigationType.COVALENTE, []),
                    (150, 1, LigationType.COVALENTE, []),
                    (210, 1, LigationType.COVALENTE, []),
                    (270, 1, LigationType.COVALENTE, []),
                    (150, 1, LigationType.COVALENTE, [])
                ]

            case 'trigonal_plana' | 'triP':
                return [
                    (270, 1, LigationType.COVALENTE, []),
                    (150, 1, LigationType.COVALENTE, []),
                    (30, 1, LigationType.COVALENTE, [])
                ]

            case 'piramidal' | 'pirA':
                return [
                    (45, 1, LigationType.COVALENTE, []),
                    (90, 1, LigationType.COVALENTE, []),
                    (135, 1, LigationType.COVALENTE, [])
                ]
            
            case 'linear' | 'linE':
                return [
                    (0, 1, LigationType.COVALENTE, []),
                    (180, 1, LigationType.COVALENTE, [])
                ]

            case 'angular_v' | 'angV':
                return [
                    (30, 1, LigationType.COVALENTE, []),
                    (135, 1, LigationType.COVALENTE, [])
                ]

            case 'binaria' | 'binA':
                return [
                    (0, 1, LigationType.COVALENTE, [])
                ]

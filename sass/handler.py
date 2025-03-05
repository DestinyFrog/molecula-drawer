from enum import Enum

class LigationType(Enum):
    COVALENTE_DATIVA = 'd'
    COVALENTE = 'c'
    IONICA = 'i'

class Handler:
    tags:list[str] = None

    def split_sections(self, text:str):
        section_tags, section_atoms, section_ligations = text.strip().split("\n\n")
        return section_tags, section_atoms, section_ligations
    
    def handle_tags(self, tags:list[str]):
        eletrons = 1
        type = LigationType.COVALENTE

        if len(tags) == 1:
            first_tag = tags[0]
            eletrons = self.match_eletrons(first_tag)

            if eletrons is None:
                eletrons = 1
                type = self.match_ligation_type(first_tag)
        elif len(tags) == 2:
            [eletrons_txt, type_txt] = tags
            eletrons = self.match_eletrons(eletrons_txt)
            type = self.match_ligation_type(type_txt)

        return eletrons, type

    def match_eletrons(self, text:str):
        match text:
            case '%':
                return 3
            case '=':
                return 2
            case '-':
                return 1
        return None

    def match_ligation_type(self, text:str):
        match text:
            case 'd':
                return LigationType.COVALENTE_DATIVA
            case 'c':
                return LigationType.COVALENTE
            case 'i':
                return LigationType.IONICA
        return None

    def match_patterns(self, text:str) -> list[float]:
        match text:
            case 'tetraedrica' | 'tetR':
                return [ 30, 150, 270 ]

            case 'trigonal_plana' | 'triP':
                return [ 270, 150, 30 ]

            case 'piramidal' | 'pirA':
                return [ 45, 90, 135 ]
            
            case 'linear' | 'linE':
                return [ 0, 180 ]

            case 'angular_v' | 'angV':
                return [ 30, 150 ]
            
            case 'linear' | 'linE':
                return [ 0, 180 ]

            case 'binaria' | 'binA':
                return [ 0 ]


    def build_ligation(self, angle:float, eletrons:int, type:LigationType):
        return (angle, eletrons, type, [])

    def handle_section_ligations(self, section:str):
        lines = section.split("\n")
        ligations = []

        for line in lines:
            angle_or_pattern, *tags = line.split(" ")

            if angle_or_pattern.isnumeric():
                angle = float(angle_or_pattern)
                eletrons, type = self.handle_tags(tags)
                ligation = self.build_ligation(angle, eletrons, type)
                ligations.append(ligation)
            else:
                pattern = self.match_patterns(angle_or_pattern)
                for angle in pattern:
                    ligation = self.build_ligation(angle, 1, LigationType.COVALENTE)
                    ligations.append(ligation)

        return ligations

    def handle_section_atoms(self, section:str, ligations):
        atoms = []
        lines = section.split("\n")

        for line_atom in lines:
            [ symbol, *atom_ligations ] = line_atom.split(" ")

            idx = len(atoms)
            atom = (symbol)
            atoms.append(atom)

            for ligation in atom_ligations:
                ligation = int(ligation) - 1
                ligations[ligation][3].append(idx)

        return atoms
    
    def handle_section_tags(self, text:str):
        return text.split(" ")
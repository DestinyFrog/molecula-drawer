from handler.ligationType import LigationType
from handler.patterns import Pattern
class SectionHandler():
    tags: list[str]
    ligations: list[(str, str, str)]
    atoms: list[str]

    def __init__(self, content:str):
        section_tags, section_atoms, section_ligations = content.split("\n\n")
        self.tags = self.handle_section_tags(section_tags)
        self.ligations = self.handle_section_ligations(section_ligations)
        self.atoms = self.handle_section_atoms(section_atoms)

    def build_ligation(self, angle:float, eletrons:int, type:LigationType):
        return (angle, eletrons, type, [])

    def handle_section_tags(self, section:str):
        return section.split(" ")
    
    def handle_atoms_tags(self, tags:list[str]):
        eletrons = 1
        type = LigationType.COVALENTE

        if len(tags) == 1:
            first_tag = tags[0]
            eletrons = self.match_eletrons(first_tag)

            if eletrons is None:
                eletrons = 1
                type = LigationType.match_ligation_type(first_tag)
        elif len(tags) == 2:
            [eletrons_txt, type_txt] = tags
            eletrons = self.match_eletrons(eletrons_txt)
            type = LigationType.match_ligation_type(type_txt)

        return eletrons, type

    def handle_section_ligations(self, section:str):
        ligations = []
        lines = section.split("\n")

        for line in lines:
            angle_or_pattern, *tags = line.split(" ")

            if angle_or_pattern.isnumeric():
                angle = float(angle_or_pattern)
                eletrons, type = self.handle_atoms_tags(tags)
                ligation = self.build_ligation(angle, eletrons, type)
                ligations.append(ligation)
            else:
                pattern = Pattern.find_pattern(angle_or_pattern)
                for ligation in pattern:
                    ligations.append(ligation)

        return ligations

    def handle_section_atoms(self, section:str) -> list[str]:
        atoms = []
        lines = section.split("\n")

        for line_atom in lines:
            symbol, *atom_ligations = line_atom.split(" ")

            idx = len(atoms)
            atom = (symbol)
            atoms.append(atom)

            for ligation in atom_ligations:
                ligation = int(ligation) - 1
                self.ligations[ligation][3].append(idx)

        return atoms

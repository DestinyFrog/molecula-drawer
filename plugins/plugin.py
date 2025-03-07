import math

from handler.handler import Handler
from handler.ligationType import LigationType
from helper.svg import Svg

class Plugin(Handler):
    standard_css = "z1.css"
    standard_template_svg = "z1.temp.svg"

    ligation_size = 26
    ligation_distance_from_atom = 7
    ligation_distance_from_ligation = 9
    triple_ligation_distance_from_ligation = 16

    border = 16

    def __init__(self, code:str):
        super(Plugin, self).__init__(code)

        self.atoms = self.handle_atoms()

        (width, height), (center_x, center_y) = self.get_bounds()
        self.width = width
        self.height = height
        self.center_x = center_x
        self.center_y = center_y

    def handle_atoms(self):
        atoms = self.handle_atoms_position(self.atoms)
        atoms.sort(key = lambda x: x[3])
        return atoms

    def handle_atoms_position(self, atoms, idx = 0, dad_atom = None, ligation = None, already = []):
        if idx in already:
            return []

        atom_symbol = atoms[idx]
        x = 0
        y = 0

        if dad_atom:
            angle = float(ligation[0])
            x = dad_atom[1] + math.cos( math.pi * angle / 180.0 ) * self.ligation_size
            y = dad_atom[2] + math.sin( math.pi * angle / 180.0 ) * self.ligation_size

        atom = [atom_symbol, x, y, idx]
        list = [atom]
        already.append(idx)

        my_ligations = filter(lambda l: l[3][0] == idx, self.ligations)
        for my_ligation in my_ligations:
            pos = self.handle_atoms_position(atoms, my_ligation[3][1], atom, my_ligation, already)
            list = list + pos

        return list

    def calculate_lines(self, a:int, b:int, angle:float, wave = [0]):
        ax = self.atoms[a][1] + self.center_x
        ay = self.atoms[a][2] + self.center_y
        bx = self.atoms[b][1] + self.center_x
        by = self.atoms[b][2] + self.center_y

        for i in wave:
            x1 = ax + math.cos( math.pi * (angle+i) / 180.0 ) * self.ligation_distance_from_atom
            y1 = ay + math.sin( math.pi * (angle+i) / 180.0 ) * self.ligation_distance_from_atom
            x2 = bx + math.cos( math.pi * (angle+180-i) / 180.0 ) * self.ligation_distance_from_atom
            y2 = by + math.sin( math.pi * (angle+180-i) / 180.0 ) * self.ligation_distance_from_atom
            yield x1, y1, x2, y2

    def eletrons_to_waves(self, eletrons: int):
        match eletrons:
            case 1:
                return [0]
            case 2:
                return [self.ligation_distance_from_ligation, -self.ligation_distance_from_ligation]
            case 3:
                return [self.triple_ligation_distance_from_ligation, 0, -self.triple_ligation_distance_from_ligation ]

    def write_atoms(self, svg:Svg) -> Svg:
        for atom in self.atoms:
            symbol, x, y, _ = atom

            if symbol == 'X':
                continue

            svg.text(symbol, x + self.center_x, y + self.center_y)

        return svg

    def write_ligations(self, svg:Svg) -> Svg:
        for ligation in self.ligations: 
            angle, eletrons, type, group = ligation

            if type == LigationType.IONICA:
                continue

            a, b = group
            if self.atoms[b][0] == 'X':
                continue
            
            wave = self.eletrons_to_waves(eletrons)

            for ax, ay, bx, by in self.calculate_lines(a, b, angle, wave):
                svg.line(ax, ay, bx, by)

        return svg

    def write(self):
        self.get_bounds()
        svg = Svg(self.width, self.height)
        svg = self.write_atoms(svg)
        svg = self.write_ligations(svg)
        return svg

    def get_bounds(self):
        small_x = 0
        small_y = 0
        big_x = 0
        big_y = 0

        for [_, x, y, _] in self.atoms:
            if small_x > x:
                small_x = x

            if small_y > y:
                small_y = y

            if big_x < x:
                big_x = x
                
            if big_y < y:
                big_y = y

        cwidth = big_x + -small_x
        cheight = big_y + -small_y

        center_x = -small_x + self.border
        center_y = -small_y + self.border
        center = (center_x, center_y)

        width = cwidth + self.border * 2
        height = cheight + self.border * 2
        size = (width, height)

        return size, center

    def get_svg(self):
        return self.write()
import math

from handler.handler import Handler, LigationType

class Plugin(Handler):
    standard_css = "z1.css"
    standard_template_svg = "z1.temp.svg"

    ligation_size = 26
    ligation_distance_from_atom = 7
    ligation_distance_from_ligation = 9
    triple_ligation_distance_from_ligation = 16
    border = 16

    svg = None
    posfix = ""

    def __init__(self, code:str):
        super(Plugin, self).__init__(code)
        
        self.atoms = self.handle_atoms()

        (width, height), (center_x, center_y) = self.get_bounds()
        self.width = width
        self.height = height
        self.center_x = center_x
        self.center_y = center_y

    def get_css(self):
        with open(self.standard_css) as file:
            style = file.read().replace("\n","").replace("\t","")
        return style

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

    def write(self):
        content = ""

        for atom in self.atoms:
            [symbol, x, y, _] = atom
            x += self.center_x
            y += self.center_y
            content += f'<text class="element element-{symbol}" x="{x}" y="{y}">{symbol}</text>'

        for ligation in self.ligations: 
            angle, eletrons, type, group = ligation
            a, b = group

            if type == LigationType.IONICA:
                continue

            ax = self.atoms[a][1] + self.center_x
            ay = self.atoms[a][2] + self.center_y
            bx = self.atoms[b][1] + self.center_x
            by = self.atoms[b][2] + self.center_y

            match eletrons:
                case 1:
                    ax = ax + math.cos( math.pi * angle / 180.0 ) * self.ligation_distance_from_atom
                    ay = ay + math.sin( math.pi * angle / 180.0 ) * self.ligation_distance_from_atom
                    bx = bx + math.cos( math.pi * (angle+180) / 180.0 ) * self.ligation_distance_from_atom
                    by = by + math.sin( math.pi * (angle+180) / 180.0 ) * self.ligation_distance_from_atom
                    content += f'<line class="ligation" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" />'

                case 2:
                    for i in [self.ligation_distance_from_ligation, -self.ligation_distance_from_ligation]:
                        ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        bx1 = bx + math.cos( math.pi * (angle+180 - i) / 180.0 ) * self.ligation_distance_from_atom
                        by1 = by + math.sin( math.pi * (angle+180 - i) / 180.0 ) * self.ligation_distance_from_atom
                        content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

                case 3:
                    for i in [self.triple_ligation_distance_from_ligation, 0, -self.triple_ligation_distance_from_ligation]:
                        ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        bx1 = bx + math.cos( math.pi * (angle+180 - i) / 180.0 ) * self.ligation_distance_from_atom
                        by1 = by + math.sin( math.pi * (angle+180 - i) / 180.0 ) * self.ligation_distance_from_atom
                        content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

        return content

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

    def build(self):
        content = self.write()

        with open(self.standard_template_svg) as file:
            svg_template = file.read()
            svg = svg_template.replace('$width', str(self.width))
            svg = svg.replace('$height', str(self.height))
            svg = svg.replace('$style', self.get_css())
            svg = svg.replace('$content', content)

        self.svg = svg

    def save(self, filename:str):
        if self.svg is not None:
            with open(f"{filename}{self.posfix}.svg", "w") as file:
                file.write(self.svg)
        else:
            raise Exception("Content not built")

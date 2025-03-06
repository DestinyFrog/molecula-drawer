import math

from plugins.plugin import Plugin
from handler.types import LigationType

class OrganicPlugin(Plugin):
    posfix = ".organic"

    def __init__(self, code:str):
        super(OrganicPlugin, self).__init__(code)

    def write(self):
        content = ""

        for atom in self.atoms:
            [symbol, x, y, _] = atom
            
            if atom[0] == 'C':
                continue
            
            if atom[0] == 'H':
                my_ligations = list(filter(lambda l: l[3][1] == atom[3], self.ligations))
                if self.atoms[my_ligations[0][3][0]][0] == 'C':
                    continue

            x += self.center_x
            y += self.center_y
            content += f'<text class="element element-{symbol}" x="{x}" y="{y}">{symbol}</text>'

        for ligation in self.ligations: 
            angle, eletrons, type, group = ligation
            a, b = group

            if type == LigationType.IONICA:
                continue

            atom_from = self.atoms[a]
            atom_to = self.atoms[b]

            if atom_from[0] == 'C' and atom_to[0] == 'H':
                continue

            ligation_distance_from = self.ligation_distance_from_atom
            ligation_distance_to = self.ligation_distance_from_atom

            if atom_from[0] == 'C':
                ligation_distance_from = 0
                
            if atom_to[0] == 'C':
                ligation_distance_to = 0

            ax = atom_from[1] + self.center_x
            ay = atom_from[2] + self.center_y
            bx = atom_to[1] + self.center_x
            by = atom_to[2] + self.center_y

            match eletrons:
                case 1:
                    ax = ax + math.cos( math.pi * angle / 180.0 ) * ligation_distance_from
                    ay = ay + math.sin( math.pi * angle / 180.0 ) * ligation_distance_from
                    bx = bx + math.cos( math.pi * (angle+180) / 180.0 ) * ligation_distance_to
                    by = by + math.sin( math.pi * (angle+180) / 180.0 ) * ligation_distance_to
                    content += f'<line class="ligation" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" />'

                case 2:
                    sum_from = -self.ligation_distance_from_ligation
                    sum_to = self.ligation_distance_from_ligation

                    if ligation_distance_from == 0:
                        ligation_distance_from = 1
                        sum_from = 90
                    
                    if ligation_distance_to == 0:
                        ligation_distance_to = 1
                        sum_to = 90

                    ax1 = ax + math.cos( math.pi * (angle + sum_from) / 180.0 ) * ligation_distance_from
                    ay1 = ay + math.sin( math.pi * (angle + sum_from) / 180.0 ) * ligation_distance_from
                    bx1 = bx + math.cos( math.pi * (angle+180 - sum_to) / 180.0 ) * ligation_distance_to
                    by1 = by + math.sin( math.pi * (angle+180 - sum_to) / 180.0 ) * ligation_distance_to
                    content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

                    ax1 = ax + math.cos( math.pi * (angle - sum_from) / 180.0 ) * ligation_distance_from
                    ay1 = ay + math.sin( math.pi * (angle - sum_from) / 180.0 ) * ligation_distance_from
                    bx1 = bx + math.cos( math.pi * (angle+180 + sum_to) / 180.0 ) * ligation_distance_to
                    by1 = by + math.sin( math.pi * (angle+180 + sum_to) / 180.0 ) * ligation_distance_to
                    content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

                case 3:
                    sum_from = -self.triple_ligation_distance_from_ligation
                    sum_to = self.triple_ligation_distance_from_ligation

                    if ligation_distance_from == 0:
                        ligation_distance_from = 2
                        sum_from = 90
                    
                    if ligation_distance_to == 0:
                        ligation_distance_to = 2
                        sum_to = 90

                    ax1 = ax + math.cos( math.pi * (angle + sum_from) / 180.0 ) * ligation_distance_from
                    ay1 = ay + math.sin( math.pi * (angle + sum_from) / 180.0 ) * ligation_distance_from
                    bx1 = bx + math.cos( math.pi * (angle+180 - sum_to) / 180.0 ) * ligation_distance_to
                    by1 = by + math.sin( math.pi * (angle+180 - sum_to) / 180.0 ) * ligation_distance_to
                    content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

                    ax1 = ax + math.cos( math.pi * (angle ) / 180.0 ) * ligation_distance_from
                    ay1 = ay + math.sin( math.pi * (angle ) / 180.0 ) * ligation_distance_from
                    bx1 = bx + math.cos( math.pi * (angle+180) / 180.0 ) * ligation_distance_to
                    by1 = by + math.sin( math.pi * (angle+180) / 180.0 ) * ligation_distance_to
                    content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

                    ax1 = ax + math.cos( math.pi * (angle - sum_from) / 180.0 ) * ligation_distance_from
                    ay1 = ay + math.sin( math.pi * (angle - sum_from) / 180.0 ) * ligation_distance_from
                    bx1 = bx + math.cos( math.pi * (angle+180 + sum_to) / 180.0 ) * ligation_distance_to
                    by1 = by + math.sin( math.pi * (angle+180 + sum_to) / 180.0 ) * ligation_distance_to
                    content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'


        return content
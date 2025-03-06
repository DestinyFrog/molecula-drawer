import math

from plugins.plugin import Plugin
from handler.types import LigationType

class LewisPlugin(Plugin):
    posfix = ".lewis"
    eletrons_radius = 0.5

    def __init__(self, code:str):
        super(LewisPlugin, self).__init__(code)

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
                    content += f'<circle class="ci-eletron" cx="{ax}" cy="{ay}" r="{self.eletrons_radius}" />'
                    
                    if type != LigationType.COVALENTE_DATIVA:
                        bx = bx + math.cos( math.pi * (angle+180) / 180.0 ) * self.ligation_distance_from_atom
                        by = by + math.sin( math.pi * (angle+180) / 180.0 ) * self.ligation_distance_from_atom
                        content += f'<circle class="ci-eletron" cx="{bx}" cy="{by}" r="{self.eletrons_radius}" />'

                case 2:
                    for i in [self.ligation_distance_from_ligation, -self.ligation_distance_from_ligation]:
                        ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        content += f'<circle class="ci-eletron" cx="{ax1}" cy="{ay1}" r="{self.eletrons_radius}" />'

                        if type != LigationType.COVALENTE_DATIVA:
                            bx1 = bx + math.cos( math.pi * (angle + 180 - i) / 180.0 ) * self.ligation_distance_from_atom
                            by1 = by + math.sin( math.pi * (angle + 180 - i) / 180.0 ) * self.ligation_distance_from_atom
                            content += f'<circle class="ci-eletron" cx="{bx1}" cy="{by1}" r="{self.eletrons_radius}" />'

                case 3:
                    for i in [self.triple_ligation_distance_from_ligation, 0, -self.triple_ligation_distance_from_ligation]:
                        ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * self.ligation_distance_from_atom
                        content += f'<circle class="ci-eletron" cx="{ax1}" cy="{ay1}" r="{self.eletrons_radius}" />'

                        if type != LigationType.COVALENTE_DATIVA:
                            bx1 = bx + math.cos( math.pi * (angle + 180 - i) / 180.0 ) * self.ligation_distance_from_atom
                            by1 = by + math.sin( math.pi * (angle + 180 - i) / 180.0 ) * self.ligation_distance_from_atom
                            content += f'<circle class="ci-eletron" cx="{bx1}" cy="{by1}" r="{self.eletrons_radius}" />'

        return content
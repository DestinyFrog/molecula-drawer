from plugins.plugin import Plugin
from handler.types import LigationType
from helper.svg import Svg

class LewisPlugin(Plugin):
    eletrons_radius = 0.5
    ligation_size = 20
    ligation_distance_from_atom = 8

    def __init__(self, code:str):
        super(LewisPlugin, self).__init__(code)

    def write_ligations(self, svg:Svg) -> Svg:
        for ligation in self.ligations: 
            angle, eletrons, type, group = ligation

            if type == LigationType.IONICA:
                continue
            
            wave = self.eletrons_to_waves(eletrons)
            a, b = group

            for ax, ay, bx, by in self.calculate_lines(a, b, angle, wave):
                svg.circle(ax, ay, self.eletrons_radius)
                svg.circle(bx, by, self.eletrons_radius)

        return svg
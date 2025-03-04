import math
import sys

filename = sys.argv[1]

ligations = []
atoms = []
ligation_size = 26
ligation_distance_from_atom = 7
ligation_distance_from_ligation = 8
triple_ligation_distance_from_ligation = 12

sp = filename.split(".")
sp.pop()
filename_not_ext = "".join(sp)

with open(filename) as file:
    ml_text = file.read()

section_tags, section_atoms, section_ligations = ml_text.strip().split("\n\n")

lines_ligations = section_ligations.split("\n")

for line_ligation in lines_ligations:
    [ angle, *eletrons ] = line_ligation.split(" ")

    el = 1
    if len(eletrons):
        match eletrons[0]:
            case '%':
                el = 3
            case '=':
                el = 2

    ligation = {
        'angle': angle,
        'el': el,
        'group': []
    }

    ligations.append(ligation)

lines_atoms = section_atoms.split("\n")

for line_atom in lines_atoms:
    [ symbol, *atom_ligations ] = line_atom.split(" ")

    idx = len(atoms)
    atoms.append(symbol)

    for ligation in atom_ligations:
        ligation = int(ligation) - 1
        ligations[ligation]['group'].append(idx)

def goPos(idx = 0, dad_atom = None, ligation = None, already = []):
    if idx in already:
        return []

    atom_symbol = atoms[idx]
    x = 0
    y = 0

    if dad_atom:
        x = dad_atom[1] + math.cos( math.pi * float(ligation["angle"]) / 180.0 ) * ligation_size
        y = dad_atom[2] + math.sin( math.pi * float(ligation["angle"]) / 180.0 ) * ligation_size

    atom = [atom_symbol, x, y, idx]
    list = [atom]
    already.append(idx)

    my_ligations = filter(lambda l: l["group"][0] == idx, ligations)
    for my_ligation in my_ligations:
        pos = goPos( my_ligation["group"][1], atom, my_ligation, already )
        list = list + pos

    return list

atoms_with_pos = goPos()
atoms_with_pos.sort(key = lambda x: x[3])

small_x = 0
small_y = 0
big_x = 0
big_y = 0
for atom in atoms_with_pos:
    x = atom[1]
    y = atom[2]
    
    if small_x > x:
        small_x = x

    if small_y > y:
        small_y = y

    if big_x < x:
        big_x = x
        
    if big_y < y:
        big_y = y

border = 16

cwidth = big_x + -small_x
cheight = big_y + -small_y

center_x = -small_x + border
center_y = -small_y + border

width = cwidth + border * 2
height = cheight + border * 2

svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'

with open("z8.css") as file:
    css = file.read().replace("\n","").replace("\t","")
    svg += f"<style>{css}</style>"

for atom in atoms_with_pos:
    symbol = atom[0]
    x = atom[1] + center_x
    y = atom[2] + center_y

    svg += f'<circle class="circle-element ci-{symbol}" cx="{x}" cy="{y}" r="{ligation_distance_from_atom}" />'
    svg += f'<text class="element {symbol}" x="{x}" y="{y}">{symbol}</text>'

for ligation in ligations: 
    angle = float( ligation["angle"] )    
    el = ligation["el"]
    a = ligation["group"][0]
    b = ligation["group"][1]
    ax = atoms_with_pos[a][1] + center_x
    ay = atoms_with_pos[a][2] + center_y
    bx = atoms_with_pos[b][1] + center_x
    by = atoms_with_pos[b][2] + center_y

    match el:
        case 1:
            ax = ax + math.cos( math.pi * angle / 180.0 ) * ligation_distance_from_atom
            ay = ay + math.sin( math.pi * angle / 180.0 ) * ligation_distance_from_atom
            bx = bx + math.cos( math.pi * (angle+180) / 180.0 ) * ligation_distance_from_atom
            by = by + math.sin( math.pi * (angle+180) / 180.0 ) * ligation_distance_from_atom
            svg += f'<line class="ligation" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" />'

        case 2:
            for i in [ligation_distance_from_ligation, -ligation_distance_from_ligation]:
                ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * ligation_distance_from_atom
                ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * ligation_distance_from_atom
                bx1 = bx + math.cos( math.pi * (angle+180 - i) / 180.0 ) * ligation_distance_from_atom
                by1 = by + math.sin( math.pi * (angle+180 - i) / 180.0 ) * ligation_distance_from_atom
                svg += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'
                
        case 3:
            for i in [triple_ligation_distance_from_ligation, 0, -triple_ligation_distance_from_ligation]:
                ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * ligation_distance_from_atom
                ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * ligation_distance_from_atom
                bx1 = bx + math.cos( math.pi * (angle+180 - i) / 180.0 ) * ligation_distance_from_atom
                by1 = by + math.sin( math.pi * (angle+180 - i) / 180.0 ) * ligation_distance_from_atom
                svg += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

svg += "</svg>"

with open(f"{filename_not_ext}.svg", "w") as file:
	file.write(svg)
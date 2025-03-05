from enum import Enum
import math
import sys
from config import config as cfg

ligation_size = 20
border = 16

filename = sys.argv[1]
sp = filename.split(".")
sp.pop()
filename_not_ext = "".join(sp)

with open(filename) as file:
    file_content = file.read()

def split_sections(text:str):
    section_tags, section_atoms, section_ligations = text.strip().split("\n\n")
    return section_tags, section_atoms, section_ligations

section_tags, section_atoms, section_ligations = split_sections(file_content)

def handle_section_tags(text:str):
    return text.split(" ")

tags = handle_section_tags(section_tags)

def match_eletrons(text:str):
    match text:
        case '%':
            return 3
        case '=':
            return 2
        case '-':
            return 1
    return None

def match_ligation_type(text:str):
    match text:
        case 'd':
            return LigationType.COVALENTE_DATIVA
        case 'c':
            return LigationType.COVALENTE
        case 'i':
            return LigationType.IONICA
    return None

def match_patterns(text:str) -> list[float]:
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

class LigationType(Enum):
    COVALENTE_DATIVA = 'd'
    COVALENTE = 'c'
    IONICA = 'i'

def build_ligation(angle:float, eletrons:int, type:LigationType):
    return (angle, eletrons, type, [])

def handle_tags(tags:list[str]):
    eletrons = 1
    type = LigationType.COVALENTE

    if len(tags) == 1:
        first_tag = tags[0]
        eletrons = match_eletrons(first_tag)

        if eletrons is None:
            eletrons = 1
            type = match_ligation_type(first_tag)
    elif len(tags) == 2:
        [eletrons_txt, type_txt] = tags
        eletrons = match_eletrons(eletrons_txt)
        type = match_ligation_type(type_txt)

    return eletrons, type

def handle_section_ligations(section:str) -> list[(float, int, LigationType)]:
    lines = section.split("\n")
    ligations = []

    for line in lines:
        angle_or_pattern, *tags = line.split(" ")

        if angle_or_pattern.isnumeric():
            angle = float(angle_or_pattern)
            eletrons, type = handle_tags(tags)
            ligation = build_ligation(angle, eletrons, type)
            ligations.append(ligation)
        else:
            pattern = match_patterns(angle_or_pattern)
            for angle in pattern:
                ligation = build_ligation(angle, 1, LigationType.COVALENTE)
                ligations.append(ligation)

    return ligations

ligations = handle_section_ligations(section_ligations)

def handle_section_atoms(section:str, ligations):
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

def handle_atoms_position(atoms, idx = 0, dad_atom = None, ligation = None, already = []):
    if idx in already:
        return []

    atom_symbol = atoms[idx]
    x = 0
    y = 0

    if dad_atom:
        angle = float(ligation[0])
        x = dad_atom[1] + math.cos( math.pi * angle / 180.0 ) * ligation_size
        y = dad_atom[2] + math.sin( math.pi * angle / 180.0 ) * ligation_size

    atom = [atom_symbol, x, y, idx]
    list = [atom]
    already.append(idx)

    my_ligations = filter(lambda l: l[3][0] == idx, ligations)
    for my_ligation in my_ligations:
        pos = handle_atoms_position(atoms, my_ligation[3][1], atom, my_ligation, already)
        list = list + pos

    return list

atoms = handle_section_atoms(section_atoms, ligations)
atoms = handle_atoms_position(atoms)
atoms.sort(key = lambda x: x[3])

def get_bounds(atoms):
    small_x = 0
    small_y = 0
    big_x = 0
    big_y = 0

    for [_, x, y, _] in atoms:        
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
    csize = (cwidth, cheight)

    center_x = -small_x + border
    center_y = -small_y + border
    center = (center_x, center_y)

    width = cwidth + border * 2
    height = cheight + border * 2
    size = (width, height)

    return csize, size, center

(cwidth, cheight), (width, height), (center_x, center_y) = get_bounds(atoms)

def write_standard(atoms, ligations):
    content = ""

    for atom in atoms:
        [symbol, x, y, _] = atom
        x += center_x
        y += center_y
        content += f'<text class="element element-{symbol}" x="{x}" y="{y}">{symbol}</text>'

    for ligation in ligations: 
        angle, eletrons, type, group = ligation
        a, b = group

        if type == LigationType.IONICA:
            continue

        ax = atoms[a][1] + center_x
        ay = atoms[a][2] + center_y
        bx = atoms[b][1] + center_x
        by = atoms[b][2] + center_y

        match eletrons:
            case 1:
                ax = ax + math.cos( math.pi * angle / 180.0 ) * cfg['ligation_distance_from_atom']
                ay = ay + math.sin( math.pi * angle / 180.0 ) * cfg['ligation_distance_from_atom']
                bx = bx + math.cos( math.pi * (angle+180) / 180.0 ) * cfg['ligation_distance_from_atom']
                by = by + math.sin( math.pi * (angle+180) / 180.0 ) * cfg['ligation_distance_from_atom']
                content += f'<line class="ligation" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" />'

            case 2:
                for i in [cfg['ligation_distance_from_ligation'], -cfg['ligation_distance_from_ligation']]:
                    ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    bx1 = bx + math.cos( math.pi * (angle+180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    by1 = by + math.sin( math.pi * (angle+180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

            case 3:
                for i in [cfg['triple_ligation_distance_from_ligation'], 0, -cfg['triple_ligation_distance_from_ligation']]:
                    ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    bx1 = bx + math.cos( math.pi * (angle+180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    by1 = by + math.sin( math.pi * (angle+180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    content += f'<line class="ligation" x1="{ax1}" y1="{ay1}" x2="{bx1}" y2="{by1}"/>'

    return content

def write_organic(atoms, ligations):
    content = ""

    for atom in atoms:
        [symbol, x, y, _] = atom
        
        if atom[0] == 'C':
            continue
        
        if atom[0] == 'H':
            my_ligations = list(filter(lambda l: l[3][1] == atom[3], ligations))
            if atoms[my_ligations[0][3][0]][0] == 'C':
                continue

        x += center_x
        y += center_y
        content += f'<text class="element element-{symbol}" x="{x}" y="{y}">{symbol}</text>'

    for ligation in ligations: 
        angle, eletrons, type, group = ligation
        a, b = group

        if type == LigationType.IONICA:
            continue

        atom_from = atoms[a]
        atom_to = atoms[b]

        if atom_from[0] == 'C' and atom_to[0] == 'H':
            continue

        ligation_distance_from = cfg['ligation_distance_from_atom']
        ligation_distance_to = cfg['ligation_distance_from_atom']

        if atom_from[0] == 'C':
            ligation_distance_from = 0
            
        if atom_to[0] == 'C':
            ligation_distance_to = 0

        ax = atom_from[1] + center_x
        ay = atom_from[2] + center_y
        bx = atom_to[1] + center_x
        by = atom_to[2] + center_y

        match eletrons:
            case 1:
                ax = ax + math.cos( math.pi * angle / 180.0 ) * ligation_distance_from
                ay = ay + math.sin( math.pi * angle / 180.0 ) * ligation_distance_from
                bx = bx + math.cos( math.pi * (angle+180) / 180.0 ) * ligation_distance_to
                by = by + math.sin( math.pi * (angle+180) / 180.0 ) * ligation_distance_to
                content += f'<line class="ligation" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" />'

            case 2:
                sum_from = -cfg["ligation_distance_from_ligation"]
                sum_to = cfg["ligation_distance_from_ligation"]

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
                sum_from = -cfg["triple_ligation_distance_from_ligation"]
                sum_to = cfg["triple_ligation_distance_from_ligation"]

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

def write_lewis(atoms, ligations):
    content = ""
    radius = 0.5

    for atom in atoms:
        [symbol, x, y, _] = atom
        x += center_x
        y += center_y
        content += f'<text class="element element-{symbol}" x="{x}" y="{y}">{symbol}</text>'

    for ligation in ligations: 
        angle, eletrons, type, group = ligation
        a, b = group

        if type == LigationType.IONICA:
            continue

        ax = atoms[a][1] + center_x
        ay = atoms[a][2] + center_y
        bx = atoms[b][1] + center_x
        by = atoms[b][2] + center_y

        match eletrons:
            case 1:
                ax = ax + math.cos( math.pi * angle / 180.0 ) * cfg['ligation_distance_from_atom']
                ay = ay + math.sin( math.pi * angle / 180.0 ) * cfg['ligation_distance_from_atom']
                content += f'<circle class="ci-eletron" cx="{ax}" cy="{ay}" r="{radius}" />'
                
                if type != LigationType.COVALENTE_DATIVA:
                    bx = bx + math.cos( math.pi * (angle+180) / 180.0 ) * cfg['ligation_distance_from_atom']
                    by = by + math.sin( math.pi * (angle+180) / 180.0 ) * cfg['ligation_distance_from_atom']
                    content += f'<circle class="ci-eletron" cx="{bx}" cy="{by}" r="{radius}" />'

            case 2:
                for i in [cfg['ligation_distance_from_ligation'], -cfg['ligation_distance_from_ligation']]:
                    ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    content += f'<circle class="ci-eletron" cx="{ax1}" cy="{ay1}" r="{radius}" />'

                    if type != LigationType.COVALENTE_DATIVA:
                        bx1 = bx + math.cos( math.pi * (angle + 180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                        by1 = by + math.sin( math.pi * (angle + 180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                        content += f'<circle class="ci-eletron" cx="{bx1}" cy="{by1}" r="{radius}" />'

            case 3:
                for i in [cfg['triple_ligation_distance_from_ligation'], 0, -cfg['triple_ligation_distance_from_ligation']]:
                    ax1 = ax + math.cos( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    ay1 = ay + math.sin( math.pi * (angle + i) / 180.0 ) * cfg['ligation_distance_from_atom']
                    content += f'<circle class="ci-eletron" cx="{ax1}" cy="{ay1}" r="{radius}" />'

                    if type != LigationType.COVALENTE_DATIVA:
                        bx1 = bx + math.cos( math.pi * (angle + 180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                        by1 = by + math.sin( math.pi * (angle + 180 - i) / 180.0 ) * cfg['ligation_distance_from_atom']
                        content += f'<circle class="ci-eletron" cx="{bx1}" cy="{by1}" r="{radius}" />'

    return content


def save(content:str, posfix:str = ""):
    with open("z8.css") as file:
        style = file.read().replace("\n","").replace("\t","")

    with open("molecula.temp.svg") as file:
        svg_template = file.read()
        svg = svg_template.replace('$width', str(width))
        svg = svg.replace('$height', str(height))
        svg = svg.replace('$style', style)
        svg = svg.replace('$content', content)

        with open(f"{filename_not_ext}{posfix}.svg", "w") as file:
            file.write(svg)

content_standard = write_standard(atoms, ligations)
save(content_standard)

content_lewis = write_lewis(atoms, ligations)
save(content_lewis, ".lewis")

if "organic" in tags:
    content_organic = write_organic(atoms, ligations)
    save(content_organic, ".organic")
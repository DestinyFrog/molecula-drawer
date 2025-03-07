from handler.ligationType import LigationType

def lig(angle:float, eletrons = 1, type = LigationType.COVALENTE):
    return (angle, eletrons, type, [])

def mult_lig(angles:list[float], eletrons = 1, type = LigationType.COVALENTE):
    return map( lambda angle : lig(angle, eletrons, type), angles )

patterns = {
    ("benZ", "benzeno"): [
        lig(30, 2),
        lig(90),
        lig(150, 2),
        lig(210),
        lig(270, 2),
        lig(150),
        lig(270),
        lig(330),
        lig(30),
        lig(90),
        lig(150),
        lig(210),
    ],

    ("hexA", "hexagon"): mult_lig([30, 90, 150, 210, 270, 150]),

    ("triP", "trigonal_plan"): mult_lig([270, 150, 30]),

    ("pirA", "piramid"): [
        lig(45),
        lig(90),
        lig(135),
        lig(270, 2, LigationType.COVALENTE_DATIVA)
    ],

    ("linE", "linear"): mult_lig([0, 180]),

    ("angV", "angular_v"): [
        lig(30),
        lig(150),
        lig(225, 2, LigationType.COVALENTE_DATIVA),
        lig(315, 2, LigationType.COVALENTE_DATIVA)
    ],

    ("binA", "binary"): mult_lig([0]),
}

class Pattern():
    def find_pattern(text:str):
        for key, value in patterns.items():
            if text in key:
                return value
        return None
import sys

# from plugins.defaultPlugin import DefaultPlugin as Plugin
from plugins.organicPlugin import OrganicPlugin as Plugin
# from plugins.lewisPlugin import LewisPlugin as Plugin

filename = sys.argv[1]

with open(filename) as file:
    file_content = file.read()

sp = filename.split(".")
sp.pop()
filename_not_ext = "".join(sp)

z1 = Plugin(file_content)
svg = z1.get_svg()
svg.save(filename_not_ext)
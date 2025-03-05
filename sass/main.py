import sys

from plugin import Plugin

filename = sys.argv[1]
with open(filename) as file:
    file_content = file.read()

filename = sys.argv[1]
sp = filename.split(".")
sp.pop()
filename_not_ext = "".join(sp)

z9 = Plugin(file_content)
z9.build()

z9.save(filename_not_ext)
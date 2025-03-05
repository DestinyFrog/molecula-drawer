
class Writer:
    standard_css = "z9.css"
    standard_template_svg = "z9.temp.svg"

    def __init__(self, filename_not_ext:str):
        self.filename_not_ext = filename_not_ext

    def get_css(self):
        with open(self.standard_css) as file:
            style = file.read().replace("\n","").replace("\t","")
        return style

    def save(self, width:int, height:int, content:str, posfix:str = ""):
        with open(self.standard_template_svg) as file:
            svg_template = file.read()
            svg = svg_template.replace('$width', str(width))
            svg = svg.replace('$height', str(height))
            svg = svg.replace('$style', self.get_css())
            svg = svg.replace('$content', content)

            with open(f"{self.filename_not_ext}{posfix}.svg", "w") as file:
                file.write(svg)
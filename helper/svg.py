
class Svg():
    width: float
    height: float
    _content: str = ''

    standard_css: str = "z1.css"
    standard_template_svg: str = "z1.temp.svg"
    posfix: str = ""

    def __init__(self, width:float, height:float):
        self.width = width
        self.height = height

    def line(self, x1:float, y1:float, x2:float, y2:float, className='ligation'):
        self._content += f'<line class="{className}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'

    def text(self, symbol:str, x:float, y:float):
        self._content += f'<text class="element element-{symbol}" x="{x}" y="{y}">{symbol}</text>'

    def circle(self, x:float, y:float, radius:float):
        self._content += f'<circle class="ci-eletron" cx="{x}" cy="{y}" r="{radius}" />'

    def get_css(self) -> str:
        with open(self.standard_css) as file:
            style = file.read().replace("\n","").replace("\t","")
        return style

    def build(self) -> str:
        with open(self.standard_template_svg) as file:
            svg_template = file.read()

            svg_template = svg_template.replace('$width', str(self.width))
            svg_template = svg_template.replace('$height', str(self.height))

            css = self.get_css()
            svg_with_css = svg_template.replace('$style', css)

            svg = svg_with_css.replace('$content', self._content)

        return svg

    def save(self, filename:str):
        svg = self.build()

        with open(f"{filename}{self.posfix}.svg", "w") as file:
            file.write(svg)
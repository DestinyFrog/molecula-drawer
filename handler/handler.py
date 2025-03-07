from handler.sectionHandler import SectionHandler

class Handler(SectionHandler):
    def __init__(self, content:str):
        super(Handler, self).__init__(content)

    def match_eletrons(self, text:str):
        match text:
            case '%':
                return 3
            case '=':
                return 2
            case '-':
                return 1
        return None

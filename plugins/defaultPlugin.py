from plugins.plugin import Plugin

class DefaultPlugin(Plugin):
    def __init__(self, code:str):
        super(DefaultPlugin, self).__init__(code)

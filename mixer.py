class Mixer():
    """Adds modules outputs together"""
    def __init__(self):
        self.modules = []
        self.v_out = 0

    def update(self):
        self.v_out = 0
        for module in self.modules:
            self.v_out += module.v_out

    def add(self, *args):
        for arg in args:
            self.modules.append(arg)

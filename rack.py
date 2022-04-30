class Rack():
    """Modular rack container"""
    def __init__(self):
        self.modules = []

    def update(self):
        for module in self.modules:
            module.update()

    def add(self, *args):
        for arg in args:
            self.modules.append(arg)
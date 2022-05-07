from graph import DiGraph

class Rack(DiGraph):
    """Modular Rack"""
    def __init__(self):
        super().__init__()
    
    def step(self):
        for node in self.order:
            self.objects[node].update()

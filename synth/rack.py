from synth.graph import DiGraph

class Rack(DiGraph):
    """Modular Rack"""
    def __init__(self):
        super().__init__()
        self.fs = 48000
    
    def step(self):
        for node in self.order:
            self.objects[node].update()

from synth.node import Node

class Mixer(Node):
    """Adds inputs"""
    def __init__(self, inputs):
        super().__init__(inputs)
        # Inputs
        self.inputs = inputs
        # Outputs
        self.outputs = [0]

    def update(self):
        self.outputs[0] = sum([inp.outputs[0] for inp in self.inputs])

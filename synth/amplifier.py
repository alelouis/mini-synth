from synth.node import Node

class Amplifier(Node):
    """Applies linear gain to module"""
    def __init__(self, value, gain):
        super().__init__([value, gain])
        # Inputs
        self.value = value
        self.gain = gain
        # Outputs
        self.outputs = [0]

    def update(self):
        self.outputs[0] = self.value.outputs[0] * self.gain.outputs[0]

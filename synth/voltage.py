from synth.node import Node


class Voltage(Node):
    """Constant voltage"""

    def __init__(self, value):
        super().__init__([])
        # Outputs
        self.outputs = [value]

    def update(self):
        pass

import math
from node import Node
        
class VCO(Node):
    """Voltage Controlled Oscillator"""
    def __init__(self, frequency, fs):
        super().__init__([frequency])
        # Inputs
        self.frequency = frequency
        # Outputs
        self.outputs = [0]
        # State
        self.fs = fs
        self.t = 0
        self.phi = 0
        
    def update(self):
        self.t += 1/self.fs
        f = self.frequency.outputs[0]  
        self.phi += 2*math.pi*f/self.fs
        self.outputs = [math.cos(self.phi)]